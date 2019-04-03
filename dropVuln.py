from joern.all import JoernSteps



def runQuery(query, type):

    results = j.runGremlinQuery(query)

    for r in results:
        print("vuln of type {type} found here \n".format(type))
        print(r)

def main():
    j = JoernSteps()

    j.setGraphDbURL("http://localhost:7474")

    j.connectToDatabase()





if __name__ == '__main__':
    main()