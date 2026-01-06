import psycopg2
import time
from datetime import datetime

def run():
    print("Starting ingestion...")
    conn = psycopg2.connect(host="postgres", dbname="cafe", user="cafe_user", password="cafe_pass")
    cur = conn.cursor()
    
    # Add Menu Items
    items = [
        (1, 'Espresso', 'coffee', 'Strong', 3.50),
        (2, 'Croissant', 'cake', 'Buttery', 4.00)
    ]
    for item in items:
        cur.execute("INSERT INTO items VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", item)
    
    # Add a sample order
    cur.execute("INSERT INTO order_items VALUES (1, 1, 2, %s) ON CONFLICT DO NOTHING", (datetime.now(),))
    
    conn.commit()
    print("Ingestion complete!")

if __name__ == "__main__":
    run()