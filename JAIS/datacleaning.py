import openai
import pandas as pd
import json
import csv
import os
data=pd.read_excel('JAIS.xlsx')
openai_api_key = os.getenv("OPENAI_API_KEY")
# print(openai_api_key)

def extract_author_address(author_address):
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
        Extract, standardize, and enrich the following author and university information. 
        Your task is to ensure consistent, deduplicated, and accurate naming across all data.

        IMPORTANT REQUIREMENTS:
        1. **Author Names**
        - Convert all names to English alphabet (transliterate non-English characters).
        - Apply title case (First Last).
        - Standardize across variations:
            - "P Prakash" → "Ponduri Prakash"
            - "Dr. John Smith" → "John Smith"
            - "Smith, John" → "John Smith"
            - "J. Smith" and "John Smith" → "John Smith"
        - Ensure one unique standardized name appears everywhere for the same person.

        2. **University Names**
        - Standardize and unify variations to the official English name.
            - Example: "WSU", "Wichita Statte University", "Wichita State University USA" 
            → "Wichita State University"
        - Translate foreign-language university names to their official English equivalent.
        - Always return the same name for the same university across records.

        3. **Location Data (State & Country)**
        - Standardize country names to official English (e.g., US/USA → "United States").
        - Standardize state/province names (e.g., CA → "California").
        - If missing, determine the correct **state and country** for the given university 
            using external knowledge (Google, world university data).
        - Ensure consistency: the same university must always map to the same state and country.

       
        CRITICAL:
        - Return only a single JSON object (not an array).
        - Use English-only text in final output.
        - Make sure author, university, state, and country are 100% consistent across all rows.

        Text to process: {author_address}

        Output format:
        {{
            "Author": "Ponduri Prakash",
            "Standardized_Author": "Ponduri Prakash", 
            "University": "Wichita State University",
            "Department": "Computer Science",
            "State": "Kansas",
            "Country": "United States",
            "Pincode": "67260"
        }}"""
   response=openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role":"system","content":"You are an expert in structured data extraction."},
            {"role":"user","content":prompt}
        ],
        temperature=0
    )
   try:
        extracted_data=response.choices[0].message.content.strip().strip('```json').strip('```')
        structured_data=json.loads(extracted_data)
        author_data={
        'Standardized_Author': structured_data.get('Standardized_Author', None),
        'University': structured_data.get('University', None),
        # 'Department': structured_data.get('Department', None),
        'State': structured_data.get('State', None),
        'Country': structured_data.get('Country', None),
        # 'Pincode': structured_data.get('Pincode', None) # assuming pincode is always present in the structured data. If not, return None.
        }
        return author_data 
   except Exception as e:
        print(e)
   return None
   


with open('extract1.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['URL','Journal_Title','Article_Title','Abstract','Author_name','Standardized_Author','Author_University','Author_State','Author_Country'])
for index,row in data.iloc[2192:2250].iterrows():
    address=row['Author_Name']+row['Author_University']
    result = extract_author_address(address)
    if not result:
        continue
    with open('extract1.csv', mode='a', newline='',encoding='utf-8') as file:
        writer=csv.writer(file)
        writer.writerow([row['ArticleURL'],'Journal of the Association for Information Systems',row['Title'],row['Abstract'],row['Author_Name'],result['Standardized_Author'],result['University'],result['State'],result['Country']])