import requests
import json
from dataclasses import dataclass
from .config import settings

cookies = settings.as_dict()['COOKIES']

headers = {
    "Csrf-Token": cookies['JSESSIONID'].replace('"',''),
    "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
}

graph_api_url = "https://www.linkedin.com/voyager/api/graphql"
people_url = "https://www.linkedin.com/m/search/results/people/"
# Obtained from https://static.licdn.com/aero-v1/sc/h/ec9l9f3nbto52cqc979odl8gw, not 100% sure if this value is static
queryid = "voyagerSearchDashClusters.15c671c3162c043443995439a3d3b6dd"

@dataclass
class Person:
    name: str
    position: str


class API:
    paging = None
    total = 0

    def __init__(self, debug):
        self.debug = debug
        self.json_output = "graph_response.json"

    def get_results(self, company_id, start=0):
        req2 = f"{graph_api_url}?variables=(start:{start},origin:COMPANY_PAGE_CANNED_SEARCH,query:(flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:currentCompany,value:List({company_id})),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&&queryId={queryid}"
        resp = requests.get(req2, cookies=cookies, headers=headers, verify=False).json()
        if self.debug:
            with open(self.json_output, 'w+') as f:
                json.dump(resp, f)
        data = resp['data']['searchDashClustersByAll']
        self.paging = data['paging']
        elements = data['elements']

        for element in elements:
            for item in element['items']:
                item = item['item']['entityResult']
                if not item:
                    continue
                try:
                    position = item['primarySubtitle']['text']
                except TypeError:
                    position = None
                yield Person(
                    name=item['title']['text'],
                    position=position,
                )

    def get_all(self, company_id):
        yield from self.get_results(company_id)
        self.total = self.paging['count']
        while self.total < self.paging['total']:
            yield from self.get_results(company_id, start=self.total)
            self.total += self.paging['count']


