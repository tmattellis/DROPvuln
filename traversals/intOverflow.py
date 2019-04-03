from joern.all import JoernSteps

j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data')

j.connectToDatabase()

myQ = '''
getCallsTo('malloc').ithArguments('0')
.sideEffect{ param = it.code }
.match{ it.type == "AdditiveExpression" }.statements()
.out("REACHES")
.match{ it.type == "CallExpression" && it.code.startsWith("memcpy") }.ithArguments("2")
.filter{ it.code != param}
.match{ it.type != "AdditiveExpression" }
.locations()
 '''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
