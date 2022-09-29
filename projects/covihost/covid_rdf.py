import rdflib
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD


g = rdflib.Graph()
g.load('import/data.rdf')


for s, p, o in g:
    print( s, p, o)
    break

print(len(g))

if (None, rdflib.URIRef('http://xmlns.com/foaf/0.1/givenNane'), None) in g:
    print("Yes")
else:
    print("NO")
"""
properties1 = []

for s, p, o in g:
    properties1.append(p)

for each in properties1:
    print(each)
"""

for s, o in g.subject_objects(RDFS.authors):
    print(o)