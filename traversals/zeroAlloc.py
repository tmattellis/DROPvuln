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

myQ = '''
arg0Source = sourceMatches('.*recv.*')
arg0Sanitizer = { it, symbol -> conditionMatches(".*%d (==| !=) 0.*",symbol)};

getCallsTo("malloc")
.taintedArgs([arg0Source])
.unchecked([arg0Sanitizer])

getCallsTo("realloc")
.taintedArgs([ANY_SOURCE, arg0Source])
.unchecked([ANY_SOURCE, arg0Sanitizer])
'''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
