dates.csv: dates ranging from 2015-08-01 to 2015-09-30

domains.csv: 100,000 random domains

input.csv: 10,000,000 records of email addresses(only domain names shown) with dates

domain-date generator.ipynb: generator for the test data.

main.py(Python integrated with SQLite3): updates another table with daily counts for each domain. Report the top 50 domains based on the percentage of increase during the past 30 days compared with total.
