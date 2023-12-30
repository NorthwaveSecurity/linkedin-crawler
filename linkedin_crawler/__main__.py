from .api import API, get_query_id
from . import write_csv
from .format_emails import email_formats
import click

@click.command()
@click.argument("company_id")
@click.argument("domain")
@click.option("--output", default="output.csv")
@click.option("--debug/--no-debug")
@click.option("-f", "--email-format", default="first.last", type=click.Choice(email_formats.keys()))
def main(company_id, output, debug, domain, email_format):
    write_csv(company_id, output, domain, email_format, debug)


if __name__ == "__main__":
    main()
