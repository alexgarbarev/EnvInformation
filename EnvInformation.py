#! /usr/bin/python

import sys, getopt, os
import plistlib
import commands
import re

def printUsage():
    print '''
    Usage: EnvInformation.py [mode] [-o|--output filepath]
    modes: 
           -w --write, writes enviroment information to plist
           -r --revert, removes enviroment information from plist
    output:
           -o --outout, optional path to plist file. If not specified, Enviroment.plist will be used. 
           If directory specified, then directory/Enviroment.plist will be used.
    ''' 
def printError(errorMessage):
    print "Error: "+errorMessage
    print "See --help or -h for help"
    sys.exit(2)

defaultPath = "Enviroment.plist"
SourceControlKey = "SourceControl"
EnviromentKey = "BuildEnviroment"

def main(argv):
    shouldWrite = False
    shouldRevert = False
    path = defaultPath
    try:
        opts, args = getopt.getopt(argv, "-rwh-o:",["write","revert","help","output"])
    except getopt.GetoptError:
        printError("Can't parse parametrs")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printUsage();
            sys.exit()
        elif opt in ("-w", "--write"):
            shouldWrite = True;
        elif opt in ("-r", "--revert"):
            shouldRevert = True
        elif opt in ("-o", "--output"):
            path = arg
    path = fixPlistPath(path)
    if shouldWrite:
        write(path)
    elif shouldRevert:
        revert(path)
    else:
        printError("Mode is not selected")



def isGitAvailable():
    return len(commands.getstatusoutput('git rev-parse')[1]) == 0
    
def getGitInfo():
    git_info = dict()
    git_info["type"] = "git"
    git_info["branch"] = commands.getstatusoutput('git rev-parse --abbrev-ref HEAD')[1]
    git_info["commit_number"] = commands.getstatusoutput('git log --oneline | wc -l | tr -d " "')[1]
    git_info["hash_short"] = commands.getstatusoutput('git rev-parse --short HEAD')[1]
    git_info["hash"] = commands.getstatusoutput('git rev-parse HEAD')[1]
    return git_info

def getSourceControlInfo():
    if isGitAvailable():
        return getGitInfo()
    else:
        return "Source control info unavailable"

def getBuildInviroment():
    env_info = dict()
    env_info["clang"] = commands.getstatusoutput('clang -v 2>&1 | head -n 1')[1]
    env_info["llvm"] = commands.getstatusoutput('llvm-gcc --version | head -n 1')[1]
    xcode_version = commands.getstatusoutput('xcodebuild -version')[1]
    env_info["xcode"] = re.sub('\s+',' ',xcode_version)
    return env_info

def fixPlistPath(filePath):
    slashSymbol = "/"
    if filePath[len(filePath)-1] == "/":
        slashSymbol = ""
    if os.path.isdir(filePath):
        filePath += slashSymbol + defaultPath
    return filePath

def plistFromPath(filePath):
    try:
        plist = plistlib.readPlist(filePath)
    except IOError, e:
        plist = dict()
        plistlib.writePlist(plist, filePath)
    return plist


def write(filePath):
    plist = plistFromPath(filePath)
    plist[SourceControlKey] = getSourceControlInfo()
    plist[EnviromentKey] = getBuildInviroment()
    plistlib.writePlist(plist, filePath)
    
def revert(filePath):
    plist = plistFromPath(filePath)
    try:
        del plist[SourceControlKey]
    except KeyError, e:
        pass
    try:
        del plist[EnviromentKey]
    except KeyError, e:
        pass

    plistlib.writePlist(plist, filePath)

if __name__ == "__main__":
   main(sys.argv[1:])
