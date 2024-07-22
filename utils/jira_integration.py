from dotenv import load_dotenv
from jira import JIRA
import logging
import os

logger = logging.getLogger(__name__)
# Load the environment variables from the .env file
load_dotenv()

# Get the master folder from the environment variable
email_jira: str = os.getenv("EMAIL_JIRA")
token: str = os.getenv("JIRA_TOKEN")
server: str = os.getenv("SERVER_JIRA")


def log_defect_to_jira(summary, description):
    jira_options = {'server': server}
    jira = JIRA(options=jira_options, basic_auth=(email_jira, token))
    print(jira)
    issue_dict = {
        'project': {'key': 'YOUR_PROJECT_KEY'},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Bug'},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    logger.info(f"Defect logged in Jira with ID: {new_issue.key}")
