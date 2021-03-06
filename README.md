# DROPvuln
DROPvuln is a work-in-progress tool (including the name) used to perform program vulnerability analysis with code property graphs

## Installation
To install, simply run the command "python tool.py install" - everything will be set up for you!

## Importing
To import, simply run the command "python tool.py import". You also have the option to import your own code using the -c flag followed by the path to your code directory.

## Running
To run the DROPvuln traversals, simply run the command "python tool.py run". You also have the option to run your own traversal using the -t flag followed by the path to your script.




# OLD DOCUMENTATION

## Requirements
To install the requirements, begin by cloning this repository. Additionally, we recommend using an VM running Ubuntu 14.04 for experimental tests on this tool. Once you've set up the virtual machine, you should ensure that Java 1.7 or 1.8 is installed - these tools will not run on newer versions!

Then, in the requirements folder, you'll find joern, Neo4j, and Gremlin. Begin installing Neo4j by decompressing the tarball, and then running the command "bin/neo4j console" when in the newly created directory for Neo4j. If Neo4j is good to run, you will see a message indicating the server is up and running on localhost:7474. 

Next, to install Gremlin, unzip the given file and copy the files from it into a directory named "gremlin-plugin" in your plugins directory for Neo4j. Note that you must create this directory yourself.

To install joern, follow the documentation here: https://joern.readthedocs.io/en/latest/installation.html . No need to worry about joern-tools, just joern itself and python joern (joern is included in the requirements folder here).

## Running the tool
Once the requirements have been set up, simply run the command "python DROPvuln.py" to run the tool/traversals. Alternatively, traversals can be run individually via the files in the "traversals" directory. 

Sample code is provided in the corresponding folder to test the traversals on, and can be inserted into the database via joern.
