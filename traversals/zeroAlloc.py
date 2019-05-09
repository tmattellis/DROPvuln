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
res_0 = j.runGremlinQuery(myQ)
for r in res_0: print(r)

myQ = '''
arg0Source = sourceMatches('.*recv.*')
arg0Sanitizer = { it, symbol -> conditionMatches(".*%d (==| !=) 0.*",symbol)};

getCallsTo("malloc")
.taintedArgs([arg0Source])
.unchecked([arg0Sanitizer])
.locations()

getCallsTo("realloc")
.taintedArgs([arg0Source])
.unchecked([arg0Sanitizer])
.locations()
'''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
