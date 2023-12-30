import json
from io import StringIO
from pathlib import Path
from linkedin_crawler import write_csv
from linkedin_crawler.api import graph_api_url, people_url

dir = Path(__file__).parent

def test_write_csv(requests_mock):
    with open(dir / 'resources' / 'graph_response.json') as f:
        requests_mock.get(graph_api_url, text=f.read())
    with open(dir / 'resources' / 'people_result.html') as f:
        requests_mock.get(people_url, text=f.read())
    company_id = 123
    domain = "example.com"
    email_format = "first.middle.last"
    with StringIO() as output:
        write_csv(company_id, output, domain, email_format)
        assert output.getvalue() == """name,first,last,email,position\r
Jan de Vries,Jan,de Vries,jan.de.vries@example.com,Does something at this company\r
"""
