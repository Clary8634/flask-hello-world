from flask import Flask
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("postgresql://lab10_me5x_user:JSlMi7SI9guF5w196lHihi8El2aFlGDx@dpg-d49qu0uuk2gs739g8ipg-a/lab10_me5x")

@app.route('/')
def index():
    return "Hello World from Clary"

@app.route('/db_test')
def db_test():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return "Database connection successful"
    except Exception as e:
        return f"Database connection failed: {e}"

@app.route('/db_create')
def db_create():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Basketball(
            First varchar(255),
            Last varchar(255),
            City varchar(255),
            Name varchar(255),
            Number int
        );
    ''')
    conn.commit()
    conn.close()
    return "Basketball Table Created"

@app.route('/db_insert')
def db_insert():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Basketball (First, Last, City, Name, Number)
        VALUES
        ('Jayson', 'Tatum', 'Boston', 'Celtics', 0),
        ('Stephen', 'Curry', 'San Francisco', 'Warriors', 30),
        ('Nikola', 'Jokic', 'Denver', 'Nuggets', 15),
        ('Kawhi', 'Leonard', 'Los Angeles', 'Clippers', 2),
        ('S', 'Clary', 'CU Boulder', 'Buffs', 3308);
    ''')
    conn.commit()
    conn.close()
    return "Basketball Table Populated"

@app.route('/db_select')
def db_select():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Basketball;")
    records = cur.fetchall()
    conn.close()

    response = "<table border='1'><tr><th>First</th><th>Last</th><th>City</th><th>Name</th><th>Number</th></tr>"
    for row in records:
        response += "<tr>" + "".join(f"<td>{str(cell)}</td>" for cell in row) + "</tr>"
    response += "</table>"
    return response

@app.route('/db_drop')
def db_drop():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Basketball;")
    conn.commit()
    conn.close()
    return "Basketball Table Dropped"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
