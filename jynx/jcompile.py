__all__ = ["JavaCompiler", "JavaCompilationError"]

import sys
import os
import array
import jynx
from javax.tools import JavaFileObject, SimpleJavaFileObject, ForwardingJavaFileManager, DiagnosticCollector
from java.io import ByteArrayInputStream, ByteArrayOutputStream
from java.lang import ClassLoader, ClassNotFoundException
from java.net import URI, URL, URLClassLoader
from com.sun.tools.javac.api import JavacTool

class JavaCompilationError(Exception):
    pass

class StringJFO(SimpleJavaFileObject):
    '''
    JavaFileObject implemention used to hold the source code.
    '''
    def __init__(self, className, codestr):
        self.codestr = codestr
        SimpleJavaFileObject.__init__(self, URI(className), JavaFileObject.Kind.SOURCE)

    def getCharContent(self, errs):
        return self.codestr

class ByteArrayJFO(SimpleJavaFileObject):
    '''
    JavaFileObject implementation used to hold the byte code.
    '''
    def __init__(self, className, kind):
        SimpleJavaFileObject.__init__(self, URI(className), kind)
        self.baos = ByteArrayOutputStream()

    def openInputStream(self):
        return ByteArrayInputStream(self.getByteArray())

    def openOutputStream(self):
        return self.baos

    def getByteArray(self):
        return self.baos.toByteArray()

class ByteJavaFileManager(ForwardingJavaFileManager):
    def __init__(self, fileManager):
        ForwardingJavaFileManager.__init__(self, fileManager)
        self.code = None

    def getJavaFileForOutput(self, location, className, kind, sibling):
        self.code = ByteArrayJFO(className, kind)
        return self.code


class ByteClassLoader(URLClassLoader):
    def __init__(self, code):
        URLClassLoader.__init__(self, [], sys.classpath._stdloader)
        self.code = code

    def findClass(self, className):
        # if className.startswith("org.python.core"):
        #     return ClassLoader.findClass(self, className)
        code = self.code.getByteArray()
        cl = self.defineClass(className, code, 0, len(code))
        if cl is None:
            raise ClassNotFoundException(className)
        else:
            return cl

def get_package(source):
    for line in source.split("\n"):
        if line.startswith("package"):
            return line.split("package")[1].split(";")[0].strip()
        elif line.startswith("class") or line.startswith("import"):
            return ""

class JavaCompiler(object):
    def __init__(self, processors = None, store = False):
        self.processors = processors
        self.store = store
        self.compiler = JavacTool.create()
        assert self.compiler, "Compiler not found"

    def compileClass(self, className, codeStr, *flags):
        diagnostics = DiagnosticCollector()
        stdFileManager = self.compiler.getStandardFileManager(diagnostics, None, None)
        jfm = ByteJavaFileManager(stdFileManager)
        flags = list(flags)
        flags.append("-cp")
        flags.append(str(sys.classpath))
        task = self.compiler.getTask(None,
                                     jfm,
                                     diagnostics,
                                     flags,
                                     None,
                                     [StringJFO(className+".java", codeStr)])
        if self.processors:
            task.setProcessors(self.processors)
            self.processors = None
        if not task.call():
            e = "\n  "+"\n  ".join(str(d) for d in diagnostics.getDiagnostics())
            raise JavaCompilationError(e)
        return jfm.code

    def createAnnotation(self, className, codeStr, *flags):
        from jannotations import annotation
        anno = self.createClass(className, codeStr, *flags)
        return annotation.extract(anno)

    def createClassFile(self, javaFile, *flags):
        fileName  = os.path.basename(javaFile)
        filePath  = os.path.dirname(javaFile)
        className = fileName[:-5]
        codeStr   = open(javaFile).read()
        compiled  = self.compileClass(className, codeStr, *flags)
        package   = get_package(codeStr)
        module    = className if not package else package+"."+className
        D = {}
        if self.store:
            code = compiled.getByteArray()
            clsfile = open(javaFile.replace(".java",".class"), "wb")
            try:
                code.tofile(clsfile)
            finally:
                clsfile.close()
            sys.classpath.append(filePath)

        loader = ByteClassLoader(compiled)
        return loader.loadClass(className if not package else package+"."+className)

    def createClass(self, className, codeStr, *flags):
        package = get_package(codeStr)
        if self.store:            
            if not package:
                codeStr = "package org.jynx.gen;\n"+codeStr
                package = "org.jynx.gen"

        compiled = self.compileClass(className, codeStr, *flags)

        if self.store:
            code = compiled.getByteArray()
            clsfile = open(os.path.join(jynx.genpath, className+".class"), "wb")
            try:
                code.tofile(clsfile)
            finally:
                clsfile.close()
        loader = ByteClassLoader(compiled)
        classPath = className if not package else package+"."+className
        return loader.loadClass(classPath)



if __name__ == '__main__':

    codeStr = '''
    public class %s {
        public static void main(String args[])
        {
            System.out.println("Hello "+args[0]);
        }
    }'''

    Foo = JavaCompiler().createClass("Foo", codeStr%"Foo")

    Foo.main(["Jython!"])

    class Bar(Foo):
        pass

    print Foo, Bar

    print issubclass(Bar, Foo)

    codeStr = '''
    import java.lang.Math;
    public class Prime {

        public static Boolean isPrime(double n)
        {

            for(int d=2;d<=Math.sqrt(n);d++)
            {
                if(n%d == 0)
                    return false;
            }
            return true;
        }
    }'''

    Prime = JavaCompiler(store=True).createClass("Prime", codeStr)
    assert Prime.isPrime(2) == True
    assert Prime.isPrime(9971) == False
    assert Prime.isPrime(9973) == True

    import org.jynx.gen.Prime

    codeStr = '''

    import org.jynx.gen.Prime;

    public class TestPrime {
        org.jynx.gen.Prime p;
        public static void main(String[] args)
        {
            System.out.println("Prime.isPrime(9973) = "+Prime.isPrime(9973));
        }
    }'''

    TestPrime = JavaCompiler().createClass("TestPrime", codeStr)

    TestPrime.main([])

    # source = open(os.path.join(jynxorg, "JyGateway.java")).read()
    # JavaCompiler(remove = False).createClass("JyGateway", source)

    codeStr = '''

    public class Foo {
        public static void main(String args[])
        {
            System.out.println("Hello "+args[0]);
        }
    }'''


    Foo = JavaCompiler().createClass("Foo", codeStr)

    class Bar(Foo):
        pass