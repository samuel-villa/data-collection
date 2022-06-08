import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=test user=postgres")
