#!/usr/bin/env python

import sys, getopt, glob, os, re
from subprocess import call

def new(name):
    #
    # Make a directory with the project name
    #

    call(["mkdir", name])
    # Generate blank Makefile
    print "Creating Makefile..."
    call(["touch", name+"/Makefile"])
    mf = open(name+"/Makefile", 'w')
    mf.truncate()
    mf.write("CC= g++\n")
    mf.write("OBJECTS= \n")
    mf.write("FLAGS= -O3\n\n")
    mf.write(name+":\n")
    mf.write("\t$(CC) $(OBJECTS) $(FLAGS) -o "+name+"\n\n")
    mf.write("clean:\n")
    mf.write("\trm *.o")
    mf.close()
    # Create main.cpp file
    print "Creating main.cpp..."
    call(["touch", name+"/main.cpp"])
    mf = open(name+"/main.cpp", 'w')
    mf.write("#include <iostream>\n\n\n")
    mf.write("int main(int argc, char* argv[]) {\n")
    mf.write("\tstd::cout << \"It worked!\" << std::endl;\n")
    mf.write("\treturn 0;\n")
    mf.write("}\n")
    mf.close()

def update(name):
    #
    # Manage Makefile
    #

    # Get all source files in project directory.
    files = glob.glob(name + '/*.cpp')
    files.sort()
    objectFiles = []

    # TODO Generate proper object make routines 
    
    makefile = open(name+"/Makefile", 'r').readlines()

    for sourceFile in files:
        dirName, fileName = os.path.split(sourceFile)
        fileNameNoExtension = fileName.split(".")[0]
        sourceFileFound = False

        locateIncludes = open(sourceFile, 'r').readlines()
        includes = [fileName]
        for include in locateIncludes:
            if '#include' in include:
                includes += re.findall('"([^"]*)"', include)
      
        for i, line in enumerate(makefile):
            if fileNameNoExtension+".o:" in line:
                sourceFileFound = True
                makefile[i] = fileNameNoExtension+".o: "+" ".join(includes)+ "\n"
                objectFiles.append(fileNameNoExtension+".o")

        if not sourceFileFound:
            makefile.append("\n\n")
            makefile.append(fileNameNoExtension+".o: "+" ".join(includes)+ "\n")
            makefile.append("\t$(CC) -c "+fileName+" $(FLAGS)")
            objectFiles.append(fileNameNoExtension+".o")
    
    # Add OBJECTS Bash variable
    
    mainExecutableFound = False
    for i, line in enumerate(makefile):
        if "OBJECTS=" in line:
            makefile[i] = "OBJECTS= "+ " ".join([x.split()[0] for x in objectFiles]) + "\n"
        elif name+":" in line:
            makefile[i] = name+": $(OBJECTS)\n"
 

    newMakefile = open(name+"/Makefile", 'w')
    newMakefile.writelines(makefile)
    newMakefile.close()

def main(argv):
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv):
            if i < len(sys.argv)-1:
                name = sys.argv[i+1]
        
            if   arg == "new":
                print "Creating project '" + name + "'..."
                new(name)
                update(name)

            elif arg == "update":
                print "Updating project..."
                update(name)

            elif arg == "build":
                print "building..."

            elif arg == "clean":
                print "cleaning..."
    else:
        print "Usage: projman.py [new, update, build, clean]"

if __name__ == "__main__":
    main(sys.argv)
