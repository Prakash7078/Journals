import openai
import pandas as pd
import json
import csv
import os

openai_api_key = os.getenv("OPENAI_API_KEY")

data=pd.read_excel('JMIS.xlsx')

openai.api_key=openai_api_key


def extract_author_address(Author_name,address):
    # prompt=f"""
    # Extract the following details from this web journal articles url
    # URL	Author_Name	Standardized_Name	Standardized_University	Author_University	Author_Department	Author_State	Author_Country	Author_Pincode	title
    # # If any detail is missing, return NULL for that field and make sure maintain the same name for field values to search by that. 
    # # ex: in one record US and other record USA and other record contains United States of america display common name for these 3 record values. Same for university, department, state names also if Wichita State University in one record and WSU in other record display common name to use in search operation in my website. 
    # # If it is common name I can search easily.
    
    # # URL: {address}
    
    # # Return the data in JSON format.
    # """

    prompt = f"""
        You are helping extract and normalize author information from research paper addresses.

        Your task is to:
        - Extract and return the following details from the given `author address` and `author name`:
        - AuthorName: Return a consistent, normalized author name based on previously seen author names (from the `Author_name` input).
        - Author_email: Return an email of author from the given `author_address`
        - University: Extract the university name and return it in a consistent format based on previously seen variations (e.g., treat "WSU" and "Wichita State University" as the same, always return "Wichita State University").
        - Department: Extract department from address.
        - State: Extract the state of the university and normalize it (e.g., treat "CA", "California" as the same).
        - Country: Normalize country name to a consistent form (e.g., treat "USA", "US", and "United States of America" all as "United States").

        Rules:
        - If any detail is missing or not found in the address, return `NULL` for that field.
        - Maintain **the same naming format** across all entries — useful for search and ranking consistency.
        - Use the `Author_name` provided to ensure unique naming. If a similar name has already appeared earlier (e.g., initials vs full name), always return the **same first-seen version** of the name.
        - Same rule applies to university, department, state, and country — normalize based on first appearance.
        - Output must be in **valid JSON format** with the exact field names: AuthorName, University, Department, State, Country, Pincode.

        Author_name: {Author_name}
        Address: {address}

        Return the result in JSON format.
        """

    response=openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role":"system","content":"You are an expert in structured data extraction."},
            {"role":"user","content":prompt}
        ],
        temperature=0
    )
    extracted_data=response.choices[0].message.content.strip().strip('```json').strip('```')
    try:
        structured_data=json.loads(extracted_data)
    except Exception as e:
        print(e)
    author_data={
        'Author_Name':structured_data.get('AuthorName', None),
        'Author_email':structured_data.get('Author_email', None),
        'University': structured_data.get('University', None),
        'Department': structured_data.get('Department', None),
        'State': structured_data.get('State', None),
        'Country': structured_data.get('Country', None),
        'Pincode': structured_data.get('Pincode', None) # assuming pincode is always present in the structured data. If not, return None.
    }  
    return author_data


# with open('DSS_cleaned.csv', mode='a', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['URL','Journal_Title','Volume_Issue','Month_Year','Abstract','Keywords','Author_name','Author_email','Author_Address','Author_University','Author_department','Author_State','Author_Country','Author_pincode'])
for index,row in data.iterrows():
    address=row['Author_Address']
    Author_name=row['Author_name']

    result = extract_author_address(Author_name,address)
    with open('newextract.csv', mode='a', newline='',encoding='utf-8') as file:
        writer=csv.writer(file)
        writer.writerow([row['URL'],row['Journal_Title'],row['Volume_Issue'],row['Year'],row['Abstract'],row['Keywords'],result['Author_Name'],row['Author_Address'],result['Author_email'],result['University'],result['Department'],result['State'],result['Country']])