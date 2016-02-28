# jynx

Integrating Java with Python using Jython is a breeze - but only when Java classes are used from Python 
code. There are some obstacles when we move into the opposite direction and try to pass our Python classes
through Jython into existing Java frameworks. Those frameworks might use

	* compile time Java annotations which cannot be added to Python classes
	* the System classloader which searches for files on the classpath

Jynx encompasses some of these obstacles through dynamic Java class generation. Those Java classes provide annotations 
or having the right names and living on the classpath. The basic idea is to use a Python class and the namespace
in which it is defined, collect enough information to generate a Java proxy class, generate a class file for
this class and access the original Python class from it. 

The machinery is complicated but for the Jynx user it shouldn't take more effort than adding a class decorator to
the Python class:

	@JavaClass
	class MyClass(Object):
		...  # my code

