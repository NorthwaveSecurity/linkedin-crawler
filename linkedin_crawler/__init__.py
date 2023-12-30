import csv
import logging
from .format_emails import get_email, split_name, NoNameException
from .api import API, get_query_id

def write_csv(company_id, output, domain, email_format, debug=False):
    queryid = get_query_id(company_id, debug=debug)

    api = API(debug)
    writer = csv.DictWriter(output, ['name','first','last','email','position'])
    writer.writeheader()
    for person in api.get_all(company_id, queryid):
        if person.name == "LinkedIn Member":
            continue
        try:
            names = split_name(person.name)
            writer.writerow({
                'name':person.name,
                'first': names[0],
                'last': " ".join(names[1:]),
                'email': get_email(email_format, domain, person.name),
                'position':person.position
            })
        except NoNameException:
            logging.debug("Could not parse name for: ", person)
            continue
