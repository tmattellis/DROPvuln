import sys, os

sys.path.append(os.getcwd())

from joern.all import JoernSteps
j = JoernSteps()

query = """ g.v(0).out() """
for x in j.executeGremlinCmd(query) : print x['data']

