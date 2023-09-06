import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to extract title and text from a URL and save as a text file
def extract_and_save(url_id, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        title_element = soup.find('h1', class_='entry-title')
        if title_element:
            title = title_element.text
        else:
            title = "No title found"

        # Extract text from the <div> tag with class "td-post-content tagdiv-type"
        text_element = soup.find('div', class_='td-post-content tagdiv-type')
        if text_element:
            text = text_element.get_text()
        else:
            text = "No text found"

        # Remove specific text from the extracted text
        text = text.replace("Blackcoffer Insights 46: Atishay Jain, Shaheed Sukhdev College of Business Studies (SSCBS)", "")

        # Create a folder named "output" if it doesn't exist
        if not os.path.exists('output'):
            os.makedirs('output')

        # Create a text file with URL ID as the filename in the "output" folder
        file_name = os.path.join('output', f"{url_id}.txt")
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(f"text: {text}")

        print(f"Data extracted and saved as {file_name}")
    except Exception as e:
        print(f"Error extracting data from {url}: {str(e)}")

# Load the Excel file
excel_file = "Input.xlsx"  # Replace with the path to your Excel file

# Read the Excel data
df = pd.read_excel(excel_file)

# Iterate through rows and extract data
for index, row in df.iterrows():
    url_id = str(row['URL_ID'])
    url = row['URL']
    extract_and_save(url_id, url)

print("Extraction completed. Text files saved in the 'output' folder.")