import json

from IPython.core.display_functions import display
from bs4 import BeautifulSoup
import requests
import pandas as pd
from IPython.display import HTML, display

def ucd():
    # Website
    website = "http://www.ucdenver.edu/pages/ucdwelcomepage.aspx"
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    # Grab website
    result = requests.get(website, headers=header)
    # Get content text
    html = result.text
    # Beautiful Soup using html.parser
    soup = BeautifulSoup(html, "html.parser")
    # Find all scripts with LD
    data_scripts = soup.find_all('script', {"type": "application/ld+json"})

    extracted_scripts = []
    # Loop though scripts and extract the content
    for script in data_scripts:
        # Get content using get_text
        script_content = script.get_text()
        # using json.loads to parse script data and convert to a dictionary
        json_data = json.loads(script_content)
        # Append to list
        extracted_scripts.append(json_data)
    # Convert the list of dictionaries to a json object
    json_object = json.dumps(extracted_scripts, indent=4)

    print("Json Object")
    print(json_object)

    # Extract department data from json since department info is under key department
    department_data = extracted_scripts[0].get("department", [])
    # Extract the department name, telephone, and URL into a dictionary then put the dictionary into a list.
    department_info_list = []
    for entry in department_data:
        department_info = {
            "department_name": entry["name"],
            "telephone": entry.get("telephone"),
            "url": entry.get("url")
        }
        department_info_list.append(department_info)

    # Dump the list of department dictionaries into a JSON file, indent 4 to format
    with open("output.json", 'w') as json_file:
        json.dump(department_info_list, json_file, indent=4)

    print("Extracting name, telephone and url from json object:")
    print("Output extracted as file output.json")


def covid():
    website = "https://cdphe.colorado.gov/covid-19/data"
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    # get website
    result = requests.get(website, headers=header)
    # get html
    html = result.text
    # Beautiful Soup using html.parser
    soup = BeautifulSoup(html, "html.parser")
    # find rows <tr> elements
    rows = soup.find_all('tr')
    extracted_rows = []
    for row in rows:
        table_data = row.find_all('td')
        if len(table_data) >= 2:
            covid_data = {
                "0": table_data[0].text,
                "1": table_data[1].text,
                "2": table_data[2].text
            }
            extracted_rows.append(covid_data)
    df = pd.DataFrame(extracted_rows)
    # Convert the DataFrame to an HTML table
    html_table = df.to_html()
    # Create an HTML object and display it
    html_object = HTML(html_table)
    display(html_object)

    return

def main():
    while True:
        print("1. UCD Web Scraping")
        print("2. COVID-19 Web Scraping")
        print("3. Exit")
        choice = input("Enter a choice: ")
        if choice == "1":
            ucd()
        elif choice == "2":
            covid()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Try again")


main()