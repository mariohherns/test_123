from dotenv import load_dotenv
from jira import JIRA
import logging
import os

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load the environment variables from the .env file
load_dotenv()

# Get the credentials and server URL from the environment variables
email_jira = os.getenv("EMAIL_JIRA")
token = os.getenv("JIRA_TOKEN")
server = os.getenv("SERVER_JIRA")

def log_defect_to_jira(summary, description):
    try:
        # Set up Jira client
        jira_options = {'server': server}
        jira = JIRA(options=jira_options, basic_auth=(email_jira, token))

        # Create issue dictionary
        issue_dict = {
            'project': {'key': 'YOUR_PROJECT_KEY'},
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Bug'},
        }

        # Create the issue in Jira
        new_issue = jira.create_issue(fields=issue_dict)
        logger.info(f"Defect logged in Jira with ID: {new_issue.key}")
        print(f"Defect logged in Jira with ID: {new_issue.key}")
    
    except Exception as e:
        logger.error(f"Failed to log defect in Jira: {e}")
        print(f"Failed to log defect in Jira: {e}")
