import openai
import pandas as pd
import json
import csv
import os
data=pd.read_excel('EJIS_all_articles_cleaned_v1.xlsx')
# openai_api_key = os.getenv("OPENAI_API_KEY")
# print(openai_api_key)
openai.api_key="API_KEY"

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
    Extract and standardize the following details from the given text containing author information:
    
    
        IMPORTANT LANGUAGE REQUIREMENTS:
        - Convert ALL text to English equivalents
        - Transliterate non-English characters to English alphabet (e.g., ñ→n, ü→u, é→e, ç→c)
        - Translate foreign language university names to their official English names
        - If university has both local and English names, use the English version
        - For author names with non-English characters, provide romanized/English alphabet version
        
        Fields to extract:
        - Author: Full name as mentioned in the text (converted to English alphabet)
        - Standardized_Author: Normalized English version for deduplication (follow rules below)
        - University: Full university name in English (standardize abbreviations and translate foreign names)
        - Department: Academic department in English (if mentioned, otherwise null)
        - State: State/province in English where the university is located
        - Country: Country name in standard English
        - Pincode: Postal/ZIP code (if mentioned, otherwise null)

        Author Name Standardization Rules:
        1. Convert to English alphabet (transliterate non-English characters)
        2. Use title case (First Letter Capitalized For Each Word)
        3. For names like "Rajesh R" and "Rajesh Raj" - if first name + first letter of last name matches, use the longer version
        4. Remove middle initials if a full middle name exists elsewhere for same person
        5. Handle common variations:
        - "Dr. John Smith" → "John Smith"
        - "Prof. Jane Doe" → "Jane Doe" 
        - "Smith, John" → "John Smith"
        - "J. Smith" vs "John Smith" → use "John Smith" if both refer to same person
        6. Remove extra spaces and special characters
        7. Convert accented characters: José → Jose, François → Francois, etc.

        University/Location Standardization Examples:
        - Universidad Politécnica de Madrid → "Technical University of Madrid"
        - WSU → "Wichita State University"
        - MIT → "Massachusetts Institute of Technology"
        - École Polytechnique → "Polytechnic School"
        - Université de Paris → "University of Paris"
        - Tsinghua Daxue → "Tsinghua University"
        - Universidad Nacional de Colombia → "National University of Colombia"
        - Technische Universität München → "Technical University of Munich"
        
        Country Standardization:
        - US/USA/United States/Estados Unidos → "United States"
        - UK/United Kingdom/Inglaterra → "United Kingdom"  
        - Deutschland/Alemania → "Germany"
        - España → "Spain"
        - França/France → "France"
        - Use full English country names

        State Standardization:
        - Use full English state/province names
        - CA → "California", NY → "New York", etc.
        - Convert regional names to English equivalents

        Text to process: {author_address}

        CRITICAL: Return ONLY as a single JSON object (not array) with English text only. Example format:
        {{
            "Author": "Jose Martinez",
            "Standardized_Author": "Jose Martinez", 
            "University": "Technical University of Madrid",
            "Department": "Computer Science",
            "State": "Madrid",
            "Country": "Spain",
            "Pincode": "28040"
        }}"""
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
        'Standardized_Author': structured_data.get('Standardized_Author', None),
        'University': structured_data.get('University', None),
        'Department': structured_data.get('Department', None),
        'State': structured_data.get('State', None),
        'Country': structured_data.get('Country', None),
        'Pincode': structured_data.get('Pincode', None) # assuming pincode is always present in the structured data. If not, return None.
    }  
    return author_data


with open('extract.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['URL','Journal_Title','Article_Title','Volume_Issue','Month_Year','Abstract','Keywords','Author_name','Standardized_Author','Author_email','Author_Address','Author_University','Author_department','Author_State','Author_Country','Author_pincode'])
for index,row in data.iterrows():
    address=row['Author_name']+row['Author_Address']
    result = extract_author_address(address)
    with open('extract.csv', mode='a', newline='',encoding='utf-8') as file:
        writer=csv.writer(file)
        writer.writerow([row['URL'],row['Journal_Title'],row['Article_Title'],row['Volume_Issue'],row['Month_Year'],row['Abstract'],row['Keywords'],row['Author_name'],result['Standardized_Author'],row['Author_email'],row['Author_Address'],result['University'],result['Department'],result['State'],result['Country'],result['Pincode']])