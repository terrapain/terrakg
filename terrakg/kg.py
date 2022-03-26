from pathlib import Path
from typing import Optional, Union

from rdflib import Graph, URIRef, RDFS

from terrakg import kgc


class KG:
    def __init__(self) -> None:
        self.g = Graph()
        kg_file = Path(__file__).parent.parent / 'data' / 'terra.ttl'
        self.g.parse(kg_file)

    def first(self, result):
        """ Just return the first element in the result"""
        for row in result:
            return row

    def get_name(self, s: URIRef) -> Optional[str]:
        return self.get_object(s, RDFS.label)[2]

    def get_object(self, s: URIRef, p: URIRef) -> Optional[Union[URIRef, str]]:
        """
        Return the object value for a given subject s and property p. If
        there are multiple objects, it will return the first.
        """
        return self.first(self.g.triples((s, p, None)))[2]

    def get_contract(self, token: URIRef, chain: URIRef = kgc.COLUMBUS_5) -> dict():
        query = f"""
        PREFIX : <{kgc.PREFIX_MV}>
        
        SELECT ?contract
        WHERE {{
          <{token}> :contractAddress ?ca .
          ?ca :chain <{chain}> .
          ?ca :address ?contract .
        }}
        """
        res = self.g.query(query)
        return self.first(res).contract

    def get_swap_opportunities(self, chain: str = kgc.COLUMBUS_5):
        query = f"""
        PREFIX : <{kgc.PREFIX_MV}>
      
        SELECT ?dex ?contract ?pair ?target
        WHERE {{
          :Luna :swap ?s .
          ?s :target ?target .
          ?s :chain <{chain}> .
          ?s :exchange ?dex .
          ?s :pairAddress ?pair .
          ?target :contractAddress ?ca .
          ?ca :chain <{chain}> .
          ?ca :address ?contract
        }}
        """
        res = self.g.query(query)
        return res

    def get_luna_pair_address(self, target: URIRef, chain: str = kgc.COLUMBUS_5):
        query = f"""
        PREFIX : <{kgc.PREFIX_MV}>

        SELECT ?pair
        WHERE {{
          :Luna :swap ?s .
          ?s :target <{target}> .
          ?s :chain <{chain}> .
          ?s :pairAddress ?pair .
        }}
        """
        res = self.g.query(query)
        return self.first(res).pair
