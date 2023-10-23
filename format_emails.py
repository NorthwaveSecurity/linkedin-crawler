import re

email_formats = {
    "f.middle.last": (lambda names: names[0][0] + "." + ".".join(names[1:])),
    "first.middle.last": (lambda names: ".".join(names)),
    "f.middlelast": (lambda names: names[0][0] + "." + "".join(names[1:])),
    "first.last": (lambda names: names[0] + "." + "".join(names[1:])),
}

name_regex = re.compile(r'[\w \.\-,]+')

def split_name(name):
    return re.findall(name_regex, name)[0].replace(',', '').strip().split()


def get_email(email_format, domain, name):
    names = split_name(name)
    # Remove other initials
    names = [x for x in names if '.' not in x]

    name = email_formats[email_format](names)
    name = name.lower().replace("ö", "oe").replace("ü", "ue").replace("ä", "ae").replace("-",'')
    name = re.sub(r'[àáâãå]', 'a', name)
    name = re.sub(r'[èéêë]', 'e', name)
    name = re.sub(r'[ìíîï]', 'i', name)
    name = re.sub(r'[òóôõø]', 'o', name)
    name = re.sub(r'[ùúû]', 'u', name)
    return name + "@" + domain


if __name__ == "__main__":
    import argparse
    import csv

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("-o", "--output-file", default="emails.txt")
    parser.add_argument("-d", "--domain", required=True)
    parser.add_argument("-f", "--email-format", default="first.last", choices=email_formats.keys())
    args = parser.parse_args()

    with open(args.csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(get_email(args.email_format, args.domain, row['name']))
