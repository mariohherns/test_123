import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import logging
import os

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load the environment variables from the .env file
load_dotenv()

# Get the credentials and server URL from the environment variables # # Jira and Zephyr Scale Configuration
ZEPHYR_BASE_URL = os.getenv("ZEPHYR_BASE_URL")
PROJECT_KEY = os.getenv("PROJECT_KEY")
API_TOKEN = os.getenv("API_TOKEN")
TEST_CYCLE_KEY = os.getenv("TEST_CYCLE_KEY")
# # Jira and Zephyr Scale Configuration


AUTH_HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json',
}

def upload_test_results(test_case_key, status, cycle_key, test_case_name):
    payload = {
        "projectKey": PROJECT_KEY,
        "testCycleKey": cycle_key,
        "testCaseKey": test_case_key,
        "statusName": status,
        "name": test_case_name
    }
    print(f"payload ::{payload}")
    response = requests.post(f"{ZEPHYR_BASE_URL}/testexecutions", json=payload, headers=AUTH_HEADERS)
    if response.status_code == 201:
        print(f"Successfully uploaded result for {test_case_key}")
    else:
        print(f"Failed to upload result for {test_case_key}: {response.text}")

def run_pytest_and_upload_results():
    os.system("pytest --junitxml=reports/results.xml")

    tree = ET.parse('reports/results.xml')
    root = tree.getroot()

    test_case_counter = 1  # Initialize a counter for assigning unique numbers to test cases

    for testcase in root.iter('testcase'):
        test_case_name = testcase.attrib['name']
        test_case_key = f"{PROJECT_KEY}-T{test_case_counter}"
        status = 'Pass'
        for child in testcase:
            if child.tag in ['failure', 'error']:
                status = 'Fail'
        upload_test_results(test_case_key, status, TEST_CYCLE_KEY, test_case_name)
        test_case_counter += 1  # Increment the counter for the next test case

run_pytest_and_upload_results()


