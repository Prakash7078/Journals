import openai
import pandas as pd
import json
import csv
data=pd.read_excel('DecisionSupportSystemArticles.xlsx')

openai.api_key='API_KEY'


def extract_author_address(address):
    prompt = f"""
    Extract the following details from the given author address:
    - University
    - Department
    - State : state of the country or place of the university
    - Country
    - Pincode
    If any detail is missing, return NULL for that field and make sure maintain the same name for field values to search by that. 
    ex: in one record US and other record USA and other record contains United States of america display common name for these 3 record values. Same for university, department, state names also if Wichita State University in one record and WSU in other record display common name to use in search operation in my website. 
    If it is common name I can search easily.
    
    Address: {address}
    
    Return the data in JSON format.
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
for index,row in data[30:].iterrows():
    address=row['Author_Address']
    result = extract_author_address(address)
    with open('DSS_cleaned.csv', mode='a', newline='',encoding='utf-8') as file:
        writer=csv.writer(file)
        writer.writerow([row['URL'],row['Journal_Title'],row['Volume_Issue'],row['Month_Year'],row['Abstract'],row['Keywords'],row['Author_name'],row['Author_email'],row['Author_Address'],result['University'],result['Department'],result['State'],result['Country'],result['Pincode']])