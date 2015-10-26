Given a table 'mailing':

CREATE TABLE mailing (
	addr VARCHAR(255) NOT NULL
);

The mailing table will initially be empty.  New addresses will be added on a daily basis.  It is expected that the table will store at least 10,000,000 email addresses and 100,000 domains.

Write a Python script that updates another table which holds a daily count of email addresses by their domain name.

Use this table to report the top 50 domains by count sorted by percentage growth of the last 30 days compared to the total.

-------------------------------------------


input.csv(not in this repo due to file size): 10,000,000 records of email addresses(only domain names shown) with dates 

domain-date generator.ipynb: generator for the 'input.csv' file.

main.py(Python integrated with SQLite3): updates another table with daily counts for each domain. Report the top 50 domains based on the percentage of increase during the past 30 days compared with total.
