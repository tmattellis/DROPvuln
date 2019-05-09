import argparse as argp
import subprocess as subp
import os
import sys
import glob


def cmd(args, write=False, filepath=None):

    if(write==True):
        temp = sys.stdout
        sys.stdout = open(filepath, 'w')

        try:
            subp.check_call(args, stdout=sys.stdout)
        except subp.CalledProcessError, e:
            return 1
        except:
            print("An unknown or unrecognized error occurred")
            return 1


        sys.stdout = temp

    else:
        try:
            subp.check_call(args)
        except subp.CalledProcessError, e:
            return 1
        except:
            print("An unknown error occurred")
            return 1

    return 0

def setupTool():
    cmd(["tar", "xfzv", "requirements/neo4j-community-2.1.8-unix.tar.gz", "-C", "requirements"])
    os.mkdir("requirements/neo4j-community-2.1.8/plugins/gremlin-plugin")
    cmd(["unzip", "requirements/neo4j-gremlin-plugin-2.1-SNAPSHOT.zip", "-d", "requirements/neo4j-community-2.1.8/plugins/gremlin-plugin"])
    cmd(["tar", "xfzv", "requirements/joern-0.3.1.tar.gz", "-C", "requirements"])
    cmd(["requirements/neo4j-community-2.1.8/bin/neo4j", "start"])
    cmd(["requirements/neo4j-community-2.1.8/bin/neo4j", "stop"])

    # set up joern, joern-tools, python-joern
    cmd(["wget", "http://mlsec.org/joern/lib/lib.tar.gz", "-P", "requirements/joern-0.3.1"])
    cmd(["tar", "xfzv", "requirements/joern-0.3.1/lib.tar.gz", "-C", "requirements/joern-0.3.1"])
    cmd(["ant", "-f", "requirements/joern-0.3.1"])
    cmd(["ant", "tools", "-f", "requirements/joern-0.3.1"])
    cmd(["sudo", "apt-get", "install", "python-setuptools", "python-dev"])
    cmd(["wget", "https://github.com/fabsx00/python-joern/archive/0.3.1.tar.gz", "-P", "requirements/joern-0.3.1"])
    cmd(["tar", "xfzv", "requirements/joern-0.3.1/0.3.1.tar.gz", "-C", "requirements/joern-0.3.1"])
    cwd = os.getcwd()
    os.chdir(cwd + '/requirements/joern-0.3.1/python-joern-0.3.1')
    cmd(["sudo", "python2", "setup.py", "install"])

def importCode(codepath):
    if(os.path.exists("~/DROPvuln/requirements/joern-0.3.1/.joernIndex") == True):
        cmd(["rm", "-r", "requirements/joern-0.3.1/.joernIndex"])
	cmd(["ant","-f", "requirements/joern-0.3.1"])

    cmd(["java", "-jar", "requirements/joern-0.3.1/bin/joern.jar", codepath])

def runTool(traversal):
    cmd(["requirements/neo4j-community-2.1.8/bin/neo4j", "start"])
    cmd(["python", traversal])
    cmd(["requirements/neo4j-community-2.1.8/bin/neo4j", "stop"])

def main(): 

    myparse = argp.ArgumentParser(description='Runs the DROP Vuln tool')

    myparse.add_argument("function", help="Select which function to use in the tool", default="run")
    myparse.add_argument("-c", help="The (complete) path to the code to be imported", default="testCode")
    myparse.add_argument("-t", help="The (specified) traversal to be run", default="dropVuln.py")

    args = myparse.parse_args()

    if(args.function.lower() == "install"):
        setupTool()
    elif(args.function.lower() == "import"):
        importCode(args.c)
    elif(args.function.lower() == "run"):
        runTool(args.t)
    else:
        print("Command not recognized. Please try again.")

    exit()


if __name__ == '__main__':
    main()
