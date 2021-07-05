from pprint import pprint
from playwright.sync_api import sync_playwright

from retriever import obtain_data
from parser import parse_informational_data
from configuration import INTERESTING_JOB_TITLES, TOPICS
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



# obtain_data()
parse_informational_data()
print_obtained_data()


'''
with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    page.goto(about_argyle)

    print(page.title())
    browser.close()
'''