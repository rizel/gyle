import json
from pprint import pprint

from configuration import OUTPUT_FILE, INTERESTING_JOB_TITLES
from global_variables import *

def parse_informational_data():
    global skipped_employees, processed_employees
    global argyle_countries, argyle_languages, argyle_interesting_facts
    json_content = None

    with open(OUTPUT_FILE, 'r') as file:
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
            if job_title in INTERESTING_JOB_TITLES:
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