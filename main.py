from json import dumps
from collections import OrderedDict
from operator import itemgetter
import json
from sys import argv
from SPARQLWrapper import SPARQLWrapper, JSON


sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


def get_actors(film):

    query = """ 
        SELECT DISTINCT ?actor  ?actorLabel  WHERE {
            BIND("%s" @en AS ?recFilm)
            ?film wdt:P1476 ?recFilm.
            ?film wdt:P161 ?actor.
            minus 
               {
                   ?film wdt:P1476 ?recFilm.
                   ?film wdt:P161 ?actor.
                   ?actor wdt:P166 ?reward.
                   filter(?reward = wd:Q103618  || ?reward=wd:Q103916 || ?reward = wd:Q106291 || ?reward=wd:Q106301)
               }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } 
        }
    """
    sparql.setQuery(query % film)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


if __name__ == "__main__":
    film = "The Lord of the Rings: The Return of the King"
    results = get_actors(film)
    arr = []
    for result in results["results"]["bindings"]:
        arr.append(result["actorLabel"]["value"])
    json_file = dict()
    json_file[film] = arr
    with open('result.json', 'w') as outfile:
        json.dump(json_file, outfile, indent=4, ensure_ascii=False)