from joern.all import JoernSteps

j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data')

j.connectToDatabase()

myQ = '''
getArguments('recv', '1')
.sideEffect{ paramName = it.code;}
.filter{ it.code.matches(paramName) }
.filter{ it.code.matches('system') }
.unsanitized(
	{ it._().or(
	  _().isCheck('.*' + paramName + '.*'),
	  _().codeContains('.*;.*')
	  )}
)
.locations()
 '''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
