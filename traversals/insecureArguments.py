from joern.all import JoernSteps

j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data')

j.connectToDatabase()

myQ = '''
getCallsTo('.*printf.*').ithArguments('1')
.sideEffect{ param = it.code }
.match{ it.type != "const String" }.statements()
 '''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
