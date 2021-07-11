import requests
import time

from bs4 import BeautifulSoup
from pprint import pprint
from pathlib import Path
from random import random

from retriever import obtain_data
from parser import parse_informational_data
from github_lookup import search_in_github
from configuration import INTERESTING_JOB_TITLES, TOPICS, GITHUB_PAGE, JOB_TITLE_FOLDER
from global_variables import *


global skipped_employees, processed_employees
global argyle_countries, argyle_languages, argyle_interesting_facts
global interesting_people

for job_title in INTERESTING_JOB_TITLES:
    interesting_people[job_title] = []

def print_obtained_data():
    pprint(argyle_countries)
    pprint(argyle_languages)
    pprint(argyle_job_titles)
    # pprint(argyle_interesting_facts)
    print("skipped_employees: "+str(skipped_employees))
    print("processed_employees: "+str(processed_employees))
    pprint(interesting_people)



def process_user_data(users_data, folder_name):
    users_url   = users_data['users_url']
    username    = users_data['username']

    name        = users_data['name']
    about_user  = users_data['about_user']
    languages   = users_data['languages']

    # process webpage repositories content
    response    = requests.get(users_url)
    parsed_tree = BeautifulSoup(response.text, 'html.parser')
    file_name   = f'{JOB_TITLE_FOLDER}/{folder_name}/{name}.md'

    with open(file_name, 'w') as user_file:
        user_file.write(f'# {name}\n')
        user_file.write(f'## {username}\n')
        user_file.write(f'*{about_user}*\n\n')

        user_file.write('languages: ')
        for language in languages:
            user_file.write("[["+language+"]] ")
        user_file.write('\n')
        try:
            image_url = parsed_tree.find_all("img", class_="rounded-1 avatar-user")[0]['src']
            user_file.write(f'picture: {image_url}\n')
            print(image_url)
        except Exception as e: print(e)
        try:
            location = parsed_tree.find("li" , attrs={"itemprop":"homeLocation"}).string
            user_file.write(f'location: {location}\n')
            print(location)
        except Exception as e: 
            print('location: ')
            print(e)
        try:
            number_of_repositories  = int(parsed_tree.find(attrs={"class":"Counter"}).string)
            user_file.write(f'#### repositories: {number_of_repositories}\n')
            # print("repositories: "+number_of_repositories)
            user_file.write('\n')
        except Exception as e: 
            print('number: ')
            print(e)
        try:
            repositories = parsed_tree.find_all(attrs={"itemprop":"name codeRepository"})
            for repository in repositories:
                user_file.write(repository.string)
            user_file.write('\n')
        except Exception as e: 
            print('repositories: ')
            print(e)
        try:
            repositories_descriptions = parsed_tree.find_all(attrs={"itemprop":"description"})
            user_file.write('repositories descriptions:\n')
            for description in repositories_descriptions:
                user_file.write(description.string)
            user_file.write('\n')
        except Exception as e: 
            print('descriptions: ')
            print(e)
        try:
            repositories_languages = parsed_tree.find_all(attrs={"itemprop":"programmingLanguage"})
            user_file.write('repositories languages:\n')
            # pprint(repositories_languages)
            for coding_language_tag in repositories_languages:
                # print(type(coding_language_tag))
                parsed_coding_language  = BeautifulSoup(coding_language_tag.text, 'html.parser')
                coding_language         = parsed_coding_language.get_text()
                user_file.write("#"+coding_language+" ")
            user_file.write('\n')
        except Exception as e: 
            print('repo languages: ')
            print(e)
        try:
            # more urls, like twitter, linkedin etc
            url_tags = parsed_tree.find_all(attrs={"class":"Link--primary "})
            print(url_tags)
            user_file.write('Additional information:\n')
            for url_tag in url_tags:
                user_file.write(url_tag['href']+' \n')
        except Exception as e: 
            print('Additional info: ')
            print(e)

    


def find_data_in_github():
    for job_title in interesting_people:
        Path(f"./{JOB_TITLE_FOLDER}").mkdir(parents=True, exist_ok=True)
        Path(f"./{JOB_TITLE_FOLDER}/{job_title}").mkdir(parents=True, exist_ok=True)

        for person in interesting_people[job_title]:
            print('-----------------------------------')
            print("person to search: "+person['Name'])
            best_match              = search_in_github(person['Name'])
            best_match['name']      = person['Name']
            best_match['languages'] = person['Languages']
            if 'users_url' in best_match:
                process_user_data(best_match, job_title)
            else:
                # TODO: create this user's file with minimum data
                print("There's no best match for this user")
        time.sleep(random()*60)


# obtain_data()
parse_informational_data()
find_data_in_github()
print_obtained_data()
