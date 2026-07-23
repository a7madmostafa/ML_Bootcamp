import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrap():
    response = requests.get('https://wuzzuf.net/search/jobs/?q=machine+learning&a=hpb')
    soup = BeautifulSoup(response.content, 'lxml')

    titles = soup.find_all("h2", {'class': 'css-m604qf'})
    titles_lst = [title.a.text for title in titles]

    links = ['https://wuzzuf.net' + title.a['href'] for title in titles]

    occupations = soup.find_all("div", {'class': 'css-1lh32fc'})
    occupations_lst = [occupation.text for occupation in occupations]

    companies = soup.find_all("a", {'class': 'css-17s97q8'})
    companies_lst = [company.text for company in companies]

    specs = soup.find_all("div", {'class': 'css-y4udm8'})
    specs_lst = [spec.text for spec in specs]

    scraped_data = {}
    scraped_data['Title'] = titles_lst
    scraped_data['Link'] = links
    scraped_data['Occupation'] = occupations_lst
    scraped_data['Company'] = companies_lst
    scraped_data['Specs'] = specs_lst

    df = pd.DataFrame(scraped_data)
    df.to_csv('mljobs.csv', index=False)
    print("Jobs Scraped Successfully")
    return df

if __name__ == '__main__':
    scrap()
