import requests
import json


from configuration import ABOUT_ARGYLE, OUTPUT_FILE
from bs4 import BeautifulSoup
from pprint import pprint


# saves obtained data in a file as a stringified json
def obtain_data():
    response = requests.get(ABOUT_ARGYLE)
    parsed_tree = BeautifulSoup(response.text, 'html.parser')
    # print(parsed_tree.prettify())

    script_tags = parsed_tree.find_all('script')
    for script_tag in script_tags:
        if script_tag.string:
            try:
                # the last parsed json is the one needed.
                # json_content = json.dumps(script_tag.string)
                with open(OUTPUT_FILE, 'w') as file:
                    json.dump(script_tag.string, file)
            except Exception as e:
                print(e)
                None