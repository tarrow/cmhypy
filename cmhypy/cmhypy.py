import hypothesisapi
from pycproject.readctree import CProject
import argparse
from SPARQLWrapper import SPARQLWrapper, JSON

def payload_builder(url, annotation_content, annotation_pre=None, annotation_exact=None, annotation_suffix=None):
    if len(annotation_pre)>32:
        annotation_pre=annotation_pre[-32:]
    if len(annotation_pre)>32:
        annotation_suffix=annotation_suffix[:32]
    payload = {
        "text": annotation_content,
        "group": "__world__",
        "uri": url,
        "target": [{"source": url,
                    "selector": [{"type":"TextQuoteSelector",
                                  "prefix": annotation_pre,
                                  "exact": annotation_exact,
                                  "suffix": annotation_suffix
                                  },
                                 {"type": "TestPositionSelector", "start": None, "end": None}]
                    }]
    }
    return payload

def icun_status_from_wikidata(string):
    sparql = SPARQLWrapper("http://query.wikidata.org/sparql")
    sparql.setQuery("""
    SELECT ?statusLabel WHERE {{
    ?item wdt:P141 ?status.
    ?item rdfs:label "{}"@en
        SERVICE wikibase:label {{bd:serviceParam wikibase:language "en" .}}
}}
    """.format(string))
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    if result['results']['bindings'] and len(result['results']['bindings'])==1:
        return result['results']['bindings'][0]['statusLabel']['value']
    return None

def annotate_EuropePMC_from_CTree(ctree, H):
    if ctree.ID[0:3] == "PMC":
        url = "http://europepmc.org/articles/{}/".format(ctree.ID)
    else:
        return
    results = (ctree.show_results("species"))
    if results and "binomial" in results and results['binomial']:
        for result in results['binomial']:
            status = icun_status_from_wikidata(result['exact'])
            if status:
                annotation = "according to wikidata " + result['exact'] + " has IUCN redlist status: " + status
                pre_tidy = result['pre'].replace("( ", "(")
                post_tidy = result['post'].replace("( ", "(")
                payload=payload_builder(url, annotation, pre_tidy, result['exact'], post_tidy)
                H.create(payload)



parser = argparse.ArgumentParser(description='Read Mined Terms from ContentMine and'
                                             ' Annotate documents online with Hypothesis')
parser.add_argument("cproject", help="name of the cproject to work on")
parser.add_argument("-u", help="your hypothes.is username", dest="user", action="store", required=True)
parser.add_argument("-k", help="your hypothes.is apikey", dest="api_key", action="store", required=True)
args=parser.parse_args()

print("Writing annotations to hypothes.is with user: {} and api key: {}". format(
    args.user, args.api_key
))

H = hypothesisapi.API(args.user, args.api_key)

cproject = CProject("./", args.cproject)


for ctree in cproject.get_ctrees():
    #annotate_EuropePMC_from_CTree(ctree, H)
    pass