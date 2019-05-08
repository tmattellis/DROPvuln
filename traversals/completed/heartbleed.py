from joern.all import JoernSteps

j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data')

j.connectToDatabase()

myQ = '''
arg3Source = sourceMatches('.*n2s.*');
arg2Sanitizer = { it, symbol -> conditionMatches(".*%s (==| !=) NULL.*", symbol)};
arg3Sanitizer = { it, symbol -> conditionMatches(".*%s.* +(d+).*", symbol)};

getCallsTo("memcpy")
.taintedArgs([ANY_SOURCE,ANY_SOURCE,arg3Source])
.unchecked([ANY_SOURCE, arg2Sanitizer, arg3Sanitizer])
 '''

res = j.runGremlinQuery(myQ)

for r in res: print(r)
