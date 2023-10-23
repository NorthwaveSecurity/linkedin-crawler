# LinkedIn Crawler

Obtain employee names and email addresses based on linked-in data

## Usage

Copy config.sample.py to config.py and set the cookie values based on the values of a logged-in browser session.

Search for a company's employees on LinkedIn and copy the company ID from the URL:

![linkedin search](images/linkedin_search.png)

```
python main.py <company_id> -d <email_domain>
```
