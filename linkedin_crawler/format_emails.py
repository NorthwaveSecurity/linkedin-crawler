import re

email_formats = {
    "f.middle.last": (lambda names: names[0][0] + "." + ".".join(names[1:])),
    "first.middle.last": (lambda names: ".".join(names)),
    "f.middlelast": (lambda names: names[0][0] + "." + "".join(names[1:])),
    "first.last": (lambda names: names[0] + "." + "".join(names[1:])),
    "flast": (lambda names: names[0] + "".join(names[1:])),
}

name_regex = re.compile(r'[\w\.\-,]+')

def split_name(name):
    return [x.replace(',', '').strip() for x in re.findall(name_regex, name)]


class NoNameException(Exception):
    pass


def get_email(email_format, domain, name, strip_maiden_name=True):
    names = split_name(name)
    # Remove other initials
    names = [x for x in names if '.' not in x]
    if not names:
        raise NoNameException()
    # Strip maiden name
    if strip_maiden_name:
        names[-1] = names[-1].split('-')[0]

    name = email_formats[email_format](names)
    name = name.lower().replace("ö", "oe").replace("ü", "ue").replace("ä", "ae")
    if strip_maiden_name:
        name = name.replace('-','')
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
    parser.add_argument("--no-strip-maiden-name", action="store_true", help="Do not strip the maiden name")
    args = parser.parse_args()

    with open(args.csv_file) as f, open(args.output_file, 'w+') as f1:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(f1, reader.fieldnames)
        writer.writeheader()
        for row in reader:
            row['email'] = get_email(args.email_format, args.domain, row['name'], strip_maiden_name=not args.no_strip_maiden_name)
            writer.writerow(row)
