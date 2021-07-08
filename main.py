import requests

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pprint import pprint

from retriever import obtain_data
from parser import parse_informational_data
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



def process_user(context, username, about_user, user_index):
    users_page_url  = f"https://github.com/{username}?tab=repositories"
    users_page      = context.new_page()
    users_page.goto(users_page_url)
    users_page.screenshot(path=f"repositories_of_{username}.png")
    users_page.close()

    # process webpage repositories content
    response    = requests.get(users_page_url)
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


# this function executed with at least one user in the search result.
def evaluate_each_user(context, page, total_users):
    username    = page.eval_on_selector( f":nth-match(a.color-text-secondary, 1)", 'e => e.textContent')
    about_user  = None
    user_found  = False

    for user_index in range(1,total_users+1):
        # page.wait_for_selector(f":nth-match(.mb-1, {user_index})")
        about_user  = page.eval_on_selector(f":nth-match(.mb-1, {user_index})", 'e => e.textContent')
        username    = page.eval_on_selector( f":nth-match(a.color-text-secondary, {user_index})", 'e => e.textContent')
        print(username)
        # try to match the user.
        if 'argyle' in about_user:
            user_found  = True
            user_data   = process_user(context, username, about_user, user_index)
        page.wait_for_load_state('networkidle')

    if not user_found:
        # process the first user
        user_data   = process_user(context, username, about_user, 1)
        



def interact_with_github(name):
    github_fullname = f"fullname:{name}"
    title = f"Search · fullname:{name} · GitHub"
    total_users = 0

    with sync_playwright() as p:
        # browser = p.firefox.launch(headless=False, slow_mo=350)
        browser = p.firefox.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f'https://github.com/search?q=fullname%3A%22{name}%22')
        try:
            section_text = page.eval_on_selector('div.codesearch-results h3', 'e => e.textContent')
            total_users = int(section_text.split()[0])
            print(total_users)
        except:
            print('no users were found.')
        finally:
            # 'div#user_search_results '
            # process first 7 at most.
            if total_users > 7: 
                total_users = 7

            # evaluate search result's list.    
            if total_users > 0:
                evaluate_each_user(context, page, total_users)
            else:
                print("there's no user to evaluate")
            browser.close()


def find_in_github():
    interact_with_github(name)

    '''
    for job_title in interesting_people:
        for person in job_title:
            interact_with_github(person['Name'])
    '''


        


# obtain_data()
parse_informational_data()
print_obtained_data()
find_in_github()
