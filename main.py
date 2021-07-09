import requests

from bs4 import BeautifulSoup
from pprint import pprint
from pathlib import Path

from retriever import obtain_data
from parser import parse_informational_data
from github_lookup import search_in_github
from configuration import INTERESTING_JOB_TITLES, TOPICS, GITHUB_PAGE
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



def process_user(users_data):
    users_url   = users_data['users_url']
    username    = users_data['username']
    about_user  = users_data['about_user']

    # process webpage repositories content
    response    = requests.get(users_url)
    parsed_tree = BeautifulSoup(response.text, 'html.parser')
    image_url               = parsed_tree.find_all("img", class_="rounded-1 avatar-user")[0]['src']
    number_of_repositories  = int(parsed_tree.find(attrs={"class":"Counter"}).string)
    location                = parsed_tree.find("li" , attrs={"itemprop":"homeLocation"}).string

    print(image_url)
    print(number_of_repositories)
    print(about_user)
    # more urls
    rel=""
    url_tags = parsed_tree.find_all(attrs={"class":"Link--primary "})
    print(url_tags)
    for url_tag in url_tags:
        print(url_tag)
        print(url_tag['href'])

    repositories = parsed_tree.find_all(attrs={"itemprop":"name codeRepository"})
    for repo in repositories:
        print(repo.string)
    repositories_descriptions = parsed_tree.find_all(attrs={"itemprop":"description"})
    pprint(repositories_descriptions)
    repositories_languages = parsed_tree.find_all(attrs={"itemprop":"programmingLanguage"})
    pprint(repositories_languages)


def find_data_in_github():
    for job_title in interesting_people:
        Path(f"./{job_title}").mkdir(parents=True, exist_ok=True)

        for person in interesting_people[job_title]:
            print(person)
            best_match = search_in_github(person['Name'])
            if best_match is None:
                print("There's no best match for this user")
            else:
                process_user(best_match)


# obtain_data()
parse_informational_data()
find_data_in_github()
print_obtained_data()
