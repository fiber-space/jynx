##############   setting jynx on Java classpath   ################

import sys
import os

import sentinel
import jclasspath

jynxpath = os.path.dirname(sentinel.__file__)
sitepath = os.path.dirname(jynxpath)
orgpath  = os.path.join(sitepath, "org")
genpath  = os.path.join(orgpath, "jynx", "gen")
basepath = os.path.dirname(os.path.dirname(os.__file__))

import java.lang.System

sys.classpath.append(os.path.join(basepath, "jython.jar"))
sys.classpath.append(sitepath)
sys.classpath.append(orgpath)
sys.classpath.append(genpath)



##############   extending python path   #########################
sys.path.append(os.path.join(jclasspath.javahome,"lib", "tools.jar"))


##################################################################

