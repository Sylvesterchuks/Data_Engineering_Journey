
# import the needed libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from math import ceil
import datetime
import argparse

# a simple logging message
import logging


# config our logging to write to an output file
logging.basicConfig(level=logging.INFO,
                    # filename='log.log',
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    # filemode='w',
                    handlers=[
                                logging.FileHandler("debug.log"),
                                logging.StreamHandler()
                            ],
                    force=True # logging.basicConfig can be run just once, we use "force=True" to reset any previous configuration
                    )


def get_html_response(url_link):
    """
        This function takes url_link as parameter and returns a list of article 
    """
    posts_details = {}
    respond = requests.get(url_link)
    respond.raise_for_status()

    soups = BeautifulSoup(respond.content,'lxml')
    section = soups.find_all('article', class_='entry-summary grid__item grid__item--third')
    return section


def retrieve_post_info(url_link):
    """
        This function takes a list of html response as parameter and returns a dictionary of values about a post
    """
    articles = []

    section = get_html_response(url_link)
    for blog in section:
        posts_details = {}
        posts_details['date_posted'] = blog.find('div').find('time', class_='entry-date published updated').text
        try:
            posts_details['title'] = blog.find('h2').text
        except:
            posts_details['title'] = 'No title'
        try:
            posts_details['author'] = blog.find('div').find('span', class_='byline').text.capitalize()
        except:
            posts_details['author'] = 'No author'
        
        try:
            desp = blog.find('p').text.split('.')[0] 
            posts_details['description'] =  desp if desp != '' else 'No desp'
        except:
            posts_details['description'] = 'No desp'

        try:
            posts_details['number_of_comments'] = int(blog.find('div').find('span', class_='comments-link').text.split()[0])
        except:
            posts_details['number_of_comments'] = 0

        try:
            posts_details['post_link'] = blog.find('h2').a['href']
        except:
            posts_details['post_link'] = 'No link'
        articles.append(posts_details)
    return articles




def scraper(url='https://m.signalvnoise.com/search/'):
    # urls = 'https://m.signalvnoise.com/search/'

    resp = requests.get(url)
    resp.raise_for_status()

    # passing the html content and a parser as arguments to the Beautiful Soup
    soups = BeautifulSoup(resp.content,'lxml')

    # find method to retrieve contents in the archive class of the html page
    blog_list = soups.find('ul',class_='archives')

    # gets all the hyperlinks of in the above variable
    blog_list_links = [link.a['href'] for link in blog_list.find_all('li')]

    # gets all the hyperlinks of in the above variable
    blog_page_num = [int(num.text[-3:].strip('()')) for num in blog_list.find_all('li')]

    # A for loop that appends the dictionary to a list
    post_list_dict = []
    for num, link in zip(blog_page_num, blog_list_links):

        if num < 10:
            post_list_dict.extend(retrieve_post_info(link))
            # print(f'{link} Site scraped successfully!!!')
        else:
            page_num = ceil(num/10)
            for i in range(1,page_num+1):
                url_link = f'{link}page/{i}/'

                post_list_dict.extend(retrieve_post_info(url_link))
            
        logging.info(f"Scraped {link} successfully")
    print(f'Site scraped successfully!!!')
    return post_list_dict


def to_dataframe(post_list, output_name='Signal_Blog_posts', orient='records'):
    """
        A program to convert scraped post to dataframe and export them as both csv and json
    """
    df = pd.DataFrame(post_list)
    df['date_posted'] = pd.to_datetime(df['date_posted']).dt.date
    df.to_csv(f'{output_name}.csv',encoding='utf-8',index=False)
    df.to_json(f'{output_name}.json',orient=orient)

if __name__=="__main__":
    
    parser = argparse.ArgumentParser()

    # Create arguments
    parser.add_argument('-o', '--output', help="Normalize Database", default='Signal_Blog_posts')
    args = parser.parse_args()
    args = vars(args)

    post_list_dict = scraper()
    to_dataframe(post_list_dict, output_name=args['output'])
