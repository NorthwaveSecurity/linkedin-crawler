import csv
from .format_emails import get_email, split_name
from .api import API, get_query_id

def write_csv(company_id, output, domain, email_format, debug=False):
    queryid = get_query_id(company_id)

    api = API(debug)
    with open(output, 'w+') as f:
        writer = csv.DictWriter(f, ['name','first','last','email','position'])
        writer.writeheader()
        for person in api.get_all(company_id, queryid):
            if person.name == "LinkedIn Member":
                continue
            names = split_name(person.name)
            writer.writerow({
                'name':person.name,
                'first': names[0],
                'last': " ".join(names[1:]),
                'email': get_email(email_format, domain, person.name),
                'position':person.position
            })
