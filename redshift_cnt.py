import psycopg2

def connect_to_redshift():
    conn = psycopg2.connect(
        dbname='your_dbname',
        user='your_username',
        password='your_password',
        host='your_redshift_host',
        port='5439'
    )
    return conn

# Example usage
connection = connect_to_redshift()
cursor = connection.cursor()
cursor.execute("SELECT * FROM sales LIMIT 10;")
results = cursor.fetchall()
print(results)
