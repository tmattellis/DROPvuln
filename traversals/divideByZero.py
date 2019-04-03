from joern.all import JoernSteps


j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data')

j.connectToDatabase()

res = j.runGremlinQuery("g.V()")


index = [res.index(r) for r in res if r.properties['operator'] == '/']



final = [str(res[i]).split()[0][2:] for i in index]


parent = []
child = []

for f in final:
	p = j.runGremlinQuery("g.v("+str(f)+")")
	c = j.runGremlinQuery("g.v("+str(f)+").out().filter{it.childNum == '1'}.filter{it.type == 'Identifier'}.statements().in()")
	for c_i in c:
		if c_i not in child and not c_i == []:
			child.append(c_i)

	if p not in parent:
		parent.append(p)

for p in parent:
	print(p)

print(len(parent))
#.statements().in()
print("------------------------------------------------")
print(len(child))

for c in child:
	print(c)




