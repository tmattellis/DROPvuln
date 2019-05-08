from joern.all import JoernSteps

j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data')

j.connectToDatabase()

myQ = '''
getArguments('(copy_from_user OR memcpy)', '2')
.filter{ !it.argToCall().toList()[0].code.matches('.*(sizeof|min).*') }
.sideEffect{ argument = it.code; } 
.sideEffect{ dstld = it.statements().toList()[0].id; } 
.unsanitized({
	it._().or(
	  _().isCheck('.*' + Pattern.quote(argument) + '.*'),
	  _().codeContains('.*alloc.*' + Pattern.quote(argument) + '.*'),
	  _().codeContains('.*min.*')
	)
}, {it._().filter{ it.code.contains('copy_from_user')} }
)
.filter{ it.id != dstId }
.locations()


 '''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
