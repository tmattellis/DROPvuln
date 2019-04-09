from joern.all import JoernSteps



def runQuery(query, type="Placeholder"):

    results = j.runGremlinQuery(query)

    for r in results:
        print("vuln of type {type} found here \n".format(type))
        print(r)

def main():
    j = JoernSteps()

    j.setGraphDbURL("http://localhost:7474")

    j.connectToDatabase()

    queries = {
    "Buffer Overflow 1" : '''
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

    "Buffer Overflow 2" : '''
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

    "Code Injection" : '''
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
                       ''',

    "Insecure Arguments" : '''
                            getCallsTo('.*printf.*').ithArguments('1')
                            .sideEffect{ param = it.code }
                            .match{ it.type != "const String" }
                            .locations()
                           ''',

    "Integer Overflow" : '''
                            getCallsTo('malloc').ithArguments('0')
                            .sideEffect{ param = it.code }
                            .match{ it.type == "AdditiveExpression" }.statements()
                            .out("REACHES")
                            .match{ it.type == "CallExpression" && it.code.startsWith("memcpy") }.ithArguments("2")
                            .filter{ it.code != param}
                            .match{ it.type != "AdditiveExpression" }
                            .locations()
                         ''',

    "Zero-Byte Allocation" : '''
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
    }

    for myType, query in queries:
        runQuery(query, myType)

    # didn't copy in divide by zero given that it was written differently. 




if __name__ == '__main__':
    main()
