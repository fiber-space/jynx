import sys
import os
import urllib

from java.lang import ClassLoader

from java.net import URL

import sys

# operating system dependent classpath separators

import java.lang.System
classpathsep = java.lang.System.getProperty("path.separator")
classpath    = java.lang.System.getProperty("java.class.path")

javahome  = java.lang.System.getProperty("java.home")

# Why is /jre is on the java.home path? This is not helpful because 
# we want to access tools.jar, which is not in the /jre.
if javahome.endswith("jre"):
   javahome = javahome[:-4]


def pathname2url(pth):
    '''
    Transform file system path into URL using urllib.pathname2url().

    Additional changes:

    Undo replacement of ':' by '|' on WinNT. Append '/' to URLs stemming from directories.
    '''
    url = urllib.pathname2url(pth)
    if classpathsep == ";": # NT
        url = url.replace("|", ":", 1)
    if os.path.isdir(pth) and url[-1]!="/":
        url+="/"
    return url

class InstallationError(Exception):pass

class ClassPath(object):    
    '''
    Class used to manage the Java classpath for Jython. 

    An instance of ClassPath can be accessed through

        sys.classpath 

    which is added by this script.
    '''
    _instance = None

    def __init__(self):
        if ClassPath._instance:
            self.__dict__.update(ClassPath._instance.__dict__)
        else:
            if 'CLASSPATH' in os.environ:
                self._path = classpath.split(classpathsep)
            else:
                self._path = []
            self._stdloader = ClassLoader.getSystemClassLoader()
            ClassPath._instance = self

    def __iter__(self):
        return iter(self._path)

    def cli_option(self):
        return "-cp"

    def update(self, *paths):
        '''
        Appends each path in paths to the classpath.
        '''
    	for pth in paths:
    		self.append(pth)

    def append(self, pth):
        '''
        Appends a single path to the classpath.
        '''        
        if pth not in self._path:
            try:
                self._stdloader.addURL(URL("file:"+pathname2url(pth)))
            except AttributeError:
                raise InstallationError("Make sure that Jython registry file is in the directory of jython.jar\n"
                                        "                   Also set registry option 'python.security.respectJavaAccessibility' to false.")    
            self._path.append(pth)
            sys.path.append(pth)

    def __repr__(self):
        return classpathsep.join(self._path)

# define new system variable
sys.classpath = ClassPath()



