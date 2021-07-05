import requests
import io
import json

from bs4 import BeautifulSoup
from pprint import pprint

from playwright.sync_api import sync_playwright

about_argyle        = "https://argyle.com/about"
output_file         = "employees.json"
skipped_employees   = 0
processed_employees = 0

argyle_countries    = {}
argyle_job_titles   = {}
argyle_languages    = {}
argyle_interesting_facts = []

interesting_job_titles = [
    'Scanner Engineer', 
    'Scanner Engineer ',   
    'Senior Backend Engineer', 
    'Senior Backend Engineer ', 
    'Senior Software Engineer ', 
    'Software Engineer',
    'Software Engineer ',
    'System Architect',
]
# interesting people defined by job titles.
interesting_people = {}
for job_title in interesting_job_titles:
    interesting_people[job_title] = []

topics = ['youtube', 'github']


# saves obtained data in a file as a stringified json
def obtain_data():
    response = requests.get(about_argyle)
    parsed_tree = BeautifulSoup(response.text, 'html.parser')
    # print(parsed_tree.prettify())

    script_tags = parsed_tree.find_all('script')
    for script_tag in script_tags:
        if script_tag.string:
            try:
                # the last parsed json is the one needed.
                # json_content = json.dumps(script_tag.string)
                with open(output_file, 'w') as file:
                    json.dump(script_tag.string, file)
            except Exception as e:
                print(e)
                None


def parse_informational_data():
    global skipped_employees, processed_employees
    global argyle_countries, argyle_languages, argyle_interesting_facts
    json_content = None

    with open(output_file, 'r') as file:
        file_string = file.read()
        # loading the stringified json
        stringified_json = json.loads(file_string)

    # loading as a json finally.
    json_content = json.loads(stringified_json)
    # pprint(json_content)
    employees_data = json_content['props']['pageProps']['employees']
    # print(len(employees_data))
    # pprint(employees_data)

    for employee in employees_data:
        try: 
            country     = employee['Country']
            languages   = employee['Languages']
            job_title   = employee['Job Title']
            argyle_interesting_facts.append(employee['Interesting Fact'])

            # country processing
            if country in argyle_countries:
                argyle_countries[country] +=1
            else:
                argyle_countries[country] = 1

            # job title processing
            if job_title in argyle_job_titles:
                argyle_job_titles[job_title] +=1
            else:
                argyle_job_titles[job_title] = 1
            # select people
            if job_title in interesting_job_titles:
                interesting_people[job_title].append(employee)

            # languages processing
            for language in languages:
                if language in argyle_languages:
                    argyle_languages[language] +=1
                else:
                    argyle_languages[language] = 1
            processed_employees+= 1
        except Exception as e:
            print(e)





# obtain_data()
parse_informational_data()

pprint(argyle_countries)
pprint(argyle_languages)
pprint(argyle_job_titles)
# pprint(argyle_interesting_facts)
# print("skipped_employees: "+str(skipped_employees))
# print("processed_employees: "+str(processed_employees))
pprint(interesting_people)

'''
with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    page.goto(about_argyle)

    print(page.title())
    browser.close()
'''