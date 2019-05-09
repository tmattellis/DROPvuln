from joern.all import JoernSteps

j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data')

j.connectToDatabase()

myQ = '''
arg1Source =('.*recv.*');
arg1Sanitizer = {it, symbol -> conditionMatches(".*;.*" ,symbol)};

getCallsTo("system")
.taintedArgs([arg1Source])
.unchecked([arg1Sanitizer])
'''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
