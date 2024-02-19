from bs4 import BeautifulSoup
import requests
import csv

subject = 'comedy'

response = requests.get(f"https://openlibrary.org/search?subject={subject}") 

soup = BeautifulSoup(response.text, 'html.parser')

books = soup.find_all('span', class_='bookcover')

isbn_list = []

for book in books:
    a_link = book.find('a')
    href = a_link.get('href')
    if href:
        isbn = href.split('/')[-1]
        isbn_list.append(isbn)


print('isbn list', isbn_list)


# Headers for CSV files
headers = ['Book Name', 'Author', 'Publication Date', 'ISBN']

with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  #writerow: Writes headers to the first line of the CSV file.
    

    for isbn in isbn_list:
        url = f'https://openlibrary.org/isbn/{isbn}.json'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            book_title = data.get('title', 'No Information')
            
            authors = data.get('authors', [])
            author_names = []
            for author in authors:
                author_response = requests.get(f"https://openlibrary.org/{author['key']}.json")
                if author_response.status_code == 200:
                    author_data = author_response.json()
                    author_names.append(author_data.get('name', 'No Information'))
            
            authors_str = ', '.join(author_names) if author_names else 'No Information'

            publish_date = data.get('publish_date', 'No Information')
            
            writer.writerow([book_title, authors_str, publish_date, isbn])
        else:
            print(f"Data could not be fetched for {isbn}. Status code: {response.status_code}")

