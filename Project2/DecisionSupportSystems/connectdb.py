import pandas as pd
import mysql.connector

# Connect to MySQL

db = mysql.connector.connect(
        host=  "localhost",
        user= "root",
        password="root",
        database="journals"
    )
cursor = db.cursor()
# # Load Excel file
df = pd.read_excel('DSS_CLEANED.xlsx')



# Insert data into MySQL
for index, row in df[:3].iterrows():
    print("loop")
    sql = """
    INSERT INTO Journal_Articles 
    (URL, Journal_Title, Volume_Issue, Month_Year, Abstract, Keywords, 
     Author_Name, Author_Email, Author_University, Author_Department, 
     Author_State, Author_Country, Author_Pincode) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        row["URL"], row["Journal_Title"], row["Volume_Issue"], row["Month_Year"], 
        row["Abstract"], row["Keywords"], row["Author_Name"], row["Author_Email"],
        row["Author_University"], row["Author_Department"], row["Author_State"], 
        row["Author_Country"], row["Author_Pincode"]
    )
    
    cursor.execute(sql, values)

# Commit & close connection
db.commit()
cursor.close()
db.close()

print("Data inserted successfully!")