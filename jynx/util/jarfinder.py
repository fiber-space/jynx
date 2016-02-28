import os
import re

def find_jars(pth, exclude = "", recursive = True):
    '''
    Finds all jars under a given directory. 

    :param pth: python to the directory for searching for jars.
    :param recursive: if the value is True the function scans all subdirectories 
                      for jars.                      
    :param exclude: a regular expression used to match paths which should
            be excluded from search. The algorithm matches:

                a. single directory names
                b. sub-paths when / is used as a separator between pattern
                   for directory names. Please don't escape the slash / manually! 
                   It will be normalized to os.sep.
    :return: a sorted list of paths to jar-files.
    '''
    jars = {}
    excluded_paths  = []
    p_exclude = None
    if exclude:
        # normalize regular expression
        S = "\\"+sep+('\\'+os.sep).join([name for name in exclude.split("/") if name])
        # add $ to care for matching the end of the path        
        p_exclude = re.compile(S+"$")

    def visit(excluded_paths, dirname, names):                
        # if recursion is not supported only use the path which was passed to the
        # function
    	if not recursive and pth!=dirname:
    		return        	
        # exclude directories whose prefix has been already excluded
        for p in excluded_paths:
            if dirname.startswith(p):
                return          
        # exclude directories which are matched by the exclude pattern  
    	if p_exclude and p_exclude.match(dirname):
    		excluded_paths.append(dirname)
    		return
    	else:
            # be content with the rest
            for name in names:
                if name.endswith(".jar"):
                    if name not in jars:
    				    jars[name] = dirname

    os.path.walk(pth, visit, excluded_paths)
    result = []
    for name, dirname in jars.items():
        result.append(os.path.join(dirname, name))
    result.sort()
    return result


