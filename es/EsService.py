from elasticsearch import Elasticsearch

class EsService:
    
    @classmethod
    def getDocumentTotalCount(cls, esClient: Elasticsearch, index: str):
        '''
        '''
        query = {
            "query": {
                "match_all": {}
            }
        }
        
        esClient.count(body=query, index=index)