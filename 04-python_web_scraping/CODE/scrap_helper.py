
# Wuzzuf Scraping Helper

import requests
from bs4 import BeautifulSoup
import pandas as pd
import math


def find_no_of_jobs(job):
    req  = requests.get('https://wuzzuf.net/search/jobs/?a=hpb&q=' + job.replace(' ', '%20'))
    soup = BeautifulSoup(req.content, 'lxml')
    jobs = int(soup.find({'strong'}).text.replace(',', ''))
    pages = math.ceil(jobs / 15)
    return jobs, pages

def scrap_pages(query):
    num_jobs, num_pages = find_no_of_jobs(query)
    query = query.replace(' ', '%20')
    titles_lst, links_lst, occupations_lst, companies_lst, specs_lst = [], [], [], [], []
    for pageNo in range(num_pages):
        page = requests.get('https://wuzzuf.net/search/jobs/?a=hpb&q=' + query + '&start=' + str(pageNo))
        soup = BeautifulSoup(page.content, 'lxml')

        titles = soup.find_all("h2", {'class': 'css-m604qf'})
        titles_lst += [title.a.text for title in titles]
        links_lst += ['https://wuzzuf.net' + title.a['href'] for title in titles]

        occupations = soup.find_all("div", {'class': 'css-1lh32fc'})
        occupations_lst += [occupation.text for occupation in occupations]

        companies = soup.find_all("a", {'class': 'css-17s97q8'})
        companies_lst += [company.text for company in companies]

        specs = soup.find_all("div", {'class': 'css-y4udm8'})
        specs_lst += [spec.text for spec in specs]

    scraped_data = {}
    scraped_data['Title'] = titles_lst
    scraped_data['Link'] = links_lst
    scraped_data['Occupation'] = occupations_lst
    scraped_data['Company'] = companies_lst
    scraped_data['Specs'] = specs_lst

    df = pd.DataFrame(scraped_data)
    
    return scraped_data, df


def combine_dfs(dfs):
    df = pd.concat(dfs)
    df = df.drop_duplicates()
    return df

def combine_dicts(dicts):
    combined_dict = {}
    for key in dicts[0].keys():
        combined_dict[key] = []
        for dict in dicts:
            combined_dict[key] += dict[key]
    return combined_dict    

