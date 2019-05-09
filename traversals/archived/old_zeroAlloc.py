from joern.all import JoernSteps

j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data')

j.connectToDatabase()

myQ = '''
getArguments('.*alloc.*', '0')
.sideEffect{ paramName = it.code;}
.filter{ it.code.matches(paramName) }
.unsanitized(
	{ it._().or(
	  _().isCheck('.*' + paramName + '.*'),
	  _().codeContains('.*0.*')
	  )}
)
.locations()
 '''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
