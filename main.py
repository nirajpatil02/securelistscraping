import requests
from bs4 import BeautifulSoup
import csv
import os

# Function to check if an article already exists in the CSV file
def is_article_already_added(link, csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Link'] == link:
                return True
    return False

csv_file = 'article_data_without_content.csv'

# Check if the CSV file exists, and create it with the header if it doesn't
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as new_csvfile:
        fieldnames = ['Title', 'Link', 'Author', 'AuthorLink']
        writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames)
        writer.writeheader()

url = "https://securelist.com/"
response = requests.get(url)
response = response.content
soup = BeautifulSoup(response, 'html.parser')
featured_articles = soup.find_all('article', class_='c-card')
results = []

# Iterate through the featured articles and extract title, link, and author
for article in featured_articles:
    title = article.find('h3', class_='c-card__title').find('a').text
    link = article.find('h3', class_='c-card__title').find('a')['href']
    
    # Check if the article is already added to the CSV file, and skip it if so
    if is_article_already_added(link, csv_file):
        continue
    
    # Find the author element and extract author name and link if it exists
    author_elem = article.find('div', class_='c-card__authors')
    if author_elem:
        author_link = author_elem.find('a')['href']
        author_name = author_elem.find('a').find('span').text
    else:
        author_name = "N/A"
        author_link = "N/A"
    
    results.append({'Title': title, 'Link': link, 'Author': author_name, 'AuthorLink': author_link})

# Write the new results to the CSV file
with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Link', 'Author', 'AuthorLink']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # If the file is empty, write the header
    if csvfile.tell() == 0:
        writer.writeheader()
    
    for result in results:
        writer.writerow(result)
