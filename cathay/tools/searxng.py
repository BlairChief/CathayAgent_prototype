from json import dumps
import requests as re
from phi.tools import Toolkit
from phi.utils.log import logger

class Searxng(Toolkit):
    def __init__(self, language: str = 'en-US'):
        super().__init__(name='searxng')
        self.searxng_url = 'http://localhost:8080'
        self.language = language
        self.register(self.search)

    def search(self, q: str, format: str):
        params = {
            'q': q,
            'format': 'json',
            'language': self.language
        }
        self.response = re.get(self.searxng_url, params=params)
        
        if self.response.status_code == 200:
            first_ten_results = self.response.json()['results'][:10]

            cleaned_results = list()
            for result in first_ten_results:
                cleaned_results.append({
                    'url': result['url'],
                    'score': result['score'],
                    'content': result['content'],
                })

            logger.info(
                f"Search returns:\n{cleaned_results}"
            )
            
            return dumps({
                "operation": "searxng",
                "result": cleaned_results
            })
        
        logger.info(
            f"Search failed, please verify the availability of Searxng."
        )
        return dumps({
            "operation": "searxng",
            "result": None
        })