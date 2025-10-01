import csv
import logging
from .format_emails import get_email, split_name, NoNameException
from .api import API

def write_csv(company_id, output, domain, email_format, debug=False):
    api = API(debug)
    writer = csv.DictWriter(output, ['name','first','last','email','position'])
    writer.writeheader()
    for person in api.get_all(company_id):
        if person.name == "LinkedIn Member":
            continue
        try:
            names = list(split_name(person.name))
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
