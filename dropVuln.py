from joern.all import JoernSteps



def runQuery(query, type, j):

    results = j.runGremlinQuery(query)
    counter=0    

    for r in results:
	counter = counter+1
        print("vuln of type " + type + " found here 	total number: " + str(counter))
        print(r)
	print("\n\n")

def main():
    j = JoernSteps()

    j.setGraphDbURL("http://localhost:7474/db/data")

    j.connectToDatabase()

    queryNames = [ "Buffer Overflow 1", "Buffer Overflow 2", "Code Injection", "Insecure Arguments", "Integer Overflow", 
                  "Zero-Byte Allocation (malloc)", "Zero Byte Allocation (realloc)", "Heartbleed"]
    queries = [           '''
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
                          ''',

                          '''
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
                          ''',

                        '''
                            arg1Source =('.*recv.*');
			    arg1Sanitizer = {it, symbol -> conditionMatches(".*;.*" ,symbol)};

			    getCallsTo("system")
			    .taintedArgs([arg1Source])
			    .unchecked([arg1Sanitizer])
                            .locations()
                       ''',

                        '''
                            getCallsTo('.*printf.*').ithArguments('1')
                            .sideEffect{ param = it.code }
			    .out("REACHES")
                            .match{ it.type != "const String" }
                            .locations()
                           ''',

                        '''
                            getCallsTo('malloc').ithArguments('0')
                            .sideEffect{ param = it.code }
                            .match{ it.type == "AdditiveExpression" }.statements()
                            .out("REACHES")
                            .match{ it.type == "CallExpression" && it.code.startsWith("memcpy") }.ithArguments("2")
                            .filter{ it.code != param}
                            .match{ it.type != "AdditiveExpression" }
                            .locations()
                         ''',

                            '''
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
 			   ''',

			   '''
			    arg0Source = sourceMatches('.*recv.*')
			    arg0Sanitizer = { it, symbol -> conditionMatches(".*%d (==| !=) 0.*",symbol)};

			    getCallsTo("malloc")
			    .taintedArgs([arg0Source])
			    .unchecked([arg0Sanitizer])
			    .locations()

			    getCallsTo("realloc")
			    .taintedArgs([ANY_SOURCE, arg0Source])
			    .unchecked([ANY_SOURCE, arg0Sanitizer])
			    .locations()
                             ''',
			  '''
			    arg3Source = sourceMatches('.*n2s.*');
			    arg2Sanitizer = { it, symbol -> conditionMatches(".*%s (==| !=) NULL.*", symbol)};
			    arg3Sanitizer = { it, symbol -> conditionMatches(".*%s.* +(d+).*", symbol)};

			    getCallsTo("memcpy")
			    .taintedArgs([ANY_SOURCE,ANY_SOURCE,arg3Source])
			    .unchecked([ANY_SOURCE, arg2Sanitizer, arg3Sanitizer])
			    .locations()
			  '''
    ]

    for i in range(0, len(queries)):
        runQuery(queries[i], queryNames[i],j)

    # didn't copy in divide by zero given that it was written differently. 




if __name__ == '__main__':
    main()
