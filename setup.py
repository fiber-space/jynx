from distutils.core import setup, Extension
import sys

py_version_t = (2,7)
py_version_s = ".".join([str(x) for x in py_version_t])

if __name__ == '__main__':
    version_ext = ""
    if 'sdist' in sys.argv:
        version_ext = '-py'+py_version_s

    setup(
        name = 'Jynx',
        version = '0.5-jython'+version_ext,
        description = 'Jython library for Python integration with modern Java using dynamic Java compilation',
        author = 'Kay Schluehr',
        author_email = 'kay@fiber-space.de',
        url = 'http://www.fiber-space.de/',
        # download_url = 'http://code.google.com/p/jynx/',
        license = "MIT License",

        packages = ['jynx.lib',
                    'jynx.lib.hibernate',
                    'jynx.lib.hibernate.tests',
                    'jynx.lib.javaparser',
                    'jynx.lib.javaparser.tests',
                    'jynx.lib.junit',
                    'jynx.lib.util',
                    'jynx.tests',
                    'jynx',
                    'org.javaparser',
                    'org.junit',
                    'org.jynx',
                    'org.jynx.gen',
                    'org.slf4j',
                    'org'],
        package_data = {'jynx.lib.hibernate': ['hibernate.cfg.xml'],
                        'org.javaparser': ['COPYING',
                                           'COPYING.LESSER',
                                           'javaparser-1.0.7.jar',
                                           'readme.txt',
                                           'TypeVisitor.class',
                                           'TypeVisitor.java'],
                        'org.junit': ['junit-4.6.jar'],
                        'org.jynx': ['JyGateway.class', 'JyGateway.java'],
                        'org.jynx.gen': ['README', 'Sentinel.class', 'Sentinel.java'],
                        'org.slf4j': ['slf4j-api-1.5.8.jar',
                                      'slf4j-nop-1.5.8.jar',
                                      'slf4j-simple-1.5.8.jar']}

    )

