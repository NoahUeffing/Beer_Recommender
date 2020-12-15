import pandas as pd
from sqlalchemy import create_engine
import sqlite3

# Load Beer Data
metadata = pd.read_csv('beers.csv', low_memory=False)

# Create DB
conn = sqlite3.connect('NSLC_Beers.db')
c = conn.cursor()

# Create Table
c.execute('CREATE TABLE BEERS (Name text, Category text, Style text, IBU text, ABV text, Brewery text, Province text, Country text, Taste_Profile text, Food_Pairing text, Flavours text, Link text)')
conn.commit()

metadata.to_sql('NSLC_BEERS', conn, if_exists='replace', index=False)

# Print all entries in table
c.execute('''  
SELECT * FROM NSLC_BEERS
          ''')

# print all data base entries
for row in c.fetchall():
    print(row)
