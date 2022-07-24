from elasticsearch import Elasticsearch

'''
@author JunHyeon.Kim
@date 20220724
'''
class EsService:
    
    @classmethod
    def getDocumentTotalCount(cls, esClient: Elasticsearch, index: str)-> int:
        '''
        :param:
        :return:
        '''
        query = {
            "query": {
                "match_all": {}
            }
        }
        
        count = esClient.count(body=query, index=index)
        return count