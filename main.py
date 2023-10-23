import requests
import re
import json
import csv
from dataclasses import dataclass
from config import cookies

headers = {
    "Csrf-Token": cookies['JSESSIONID'].replace('"','')
}

def get_query_id(company_id):
    req1 = f"https://www.linkedin.com/search/results/people/?currentCompany=[\"{company_id}\"]&origin=COMPANY_PAGE_CANNED_SEARCH&sid=CL@"
    queryid_regex = re.compile("voyagerSearchDashClusters\.[^\"]+")
    resp = requests.get(req1, cookies=cookies, headers=headers)
    return queryid_regex.search(resp.text).group(0)

@dataclass
class Person:
    name: str
    position: str


class API:
    paging = None
    total = 0

    def get_results(self, company_id, queryid, start=0):
        req2 = f"https://www.linkedin.com/voyager/api/graphql?variables=(start:{start},origin:COMPANY_PAGE_CANNED_SEARCH,query:(flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:currentCompany,value:List({company_id})),(key:resultType,value:List(PEOPLE))),includeFiltersInResponse:false))&&queryId={queryid}"
        resp = requests.get(req2, cookies=cookies, headers=headers)
        data = resp.json()['data']['searchDashClustersByAll']
        self.paging = data['paging']
        elements = data['elements']

        for element in elements:
            for item in element['items']:
                item = item['item']['entityResult']
                if not item:
                    continue
                yield Person(
                    name=item['title']['text'],
                    position=item['primarySubtitle']['text'],
                )

    def get_all(self, company_id, queryid):
        yield from self.get_results(company_id, queryid)
        self.total = self.paging['count']
        while self.total < self.paging['total']:
            yield from self.get_results(company_id, queryid, start=self.total)
            self.total += self.paging['count']


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("company_id")
parser.add_argument("--output", default="output.csv")
args = parser.parse_args()

queryid = get_query_id(args.company_id)

api = API()
with open(args.output, 'w+') as f:
    writer = csv.DictWriter(f, ['name','position'])
    writer.writeheader()
    for person in api.get_all(args.company_id, queryid):
        if person.name == "LinkedIn Member":
            continue
        writer.writerow({'name':person.name, 'position':person.position})
        print(f"{person.name},{person.position}")
