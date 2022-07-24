from elasticsearch import Elasticsearch

'''
@author JunHyeon.Kim
@date 20220724
'''
class EsService:
    
    @classmethod
    def rmDocument(cls, paramDate: str):
        '''
        '''
        query = {
            "query": {
                "term" : {
                    "date_col" : {
                        "value": paramDate
                    }
                }
            }
        }

        return query

    @classmethod
    def getDateQuery(cls):
        '''
        :param:
        :return:
        '''
        query = {
            "size": 1
            ,"_source": ["date_col"]
            ,"sort": [
                {
                    "date_col.keyword": {"order": "desc"}
                }
            ]
        }
        
        return query
        
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