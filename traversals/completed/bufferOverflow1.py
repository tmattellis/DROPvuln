from joern.all import JoernSteps

j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data')

j.connectToDatabase()

myQ = '''
getFunctionASTsByName('*_write*')
.getArguments('(copy_from_user OR memcpy)', '2')
.sideEffect{ paramName = 'c(ou)?nt';}
.filter{ it.code.matches(paramName) }
.unsanitized(
	{ it._().or(
	  _().isCheck('.*' + paramName + '.*'),
	  _().codeContains('.*alloc.*' + paramName + '.*'),
	  _().codeContains('.*min.*')
	  )}
)
.param('.*c(ou)?nt')
.locations()


 '''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
