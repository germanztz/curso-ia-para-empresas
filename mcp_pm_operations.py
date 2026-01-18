from dotenv import load_dotenv
from typing import Annotated, List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool
from langchain_mcp_adapters.tools import to_fastmcp
import pandas as pd
import os
import json
import datetime

# load environment variables from .env file
load_dotenv()
workfolder = os.getenv('WORKFOLDER')
projects_df = pd.read_csv(os.path.join(workfolder, "projects.csv"))
email_reasons_df = pd.read_csv(os.path.join(workfolder, "email_reasons.csv"))


@tool
def send_email(from_email: Annotated[str, "The sender's email address."], 
    to_email:Annotated[str, "The recipient's email address."], 
    subject:Annotated[str, "The subject of the email."], 
    body:Annotated[str, "The body of the email."]
    ) -> Annotated[str, "result message"]:
    """ Sends an email."""
    try:
        now = datetime.datetime.now()
        date_string = now.strftime("%d/%m/%Y %H:%M:%S")
        email = {'date': date_string, 'from_email': from_email, 'to_email': to_email, 'tags': '', 'subject': subject, 'body': body}
        file_path = os.path.join(workfolder, "emails.csv")
        if os.path.exists(file_path):
            emails_df = pd.read_csv(file_path, index_col='id')
            emails_df = pd.concat([emails_df, pd.DataFrame([email])], ignore_index=True)
        else:
            emails_df = pd.DataFrame([email])

        emails_df.to_csv(file_path, index=True, index_label='id')
        return "email sent successfully"
    except Exception as e:
       return f"email sending failed {e}"

@tool
def get_emails() -> dict:
    """ Returns the last email received by the system, in json: {'id': 0, 'date': '', 'from_email': '', 'to_email': '', 'tags': '', 'subject': '', 'body': ''}.
    """
    emails_df = pd.read_csv(os.path.join(workfolder, "emails.csv"), index_col='id')

    # Filter for emails with empty or NaN tags
    emails_without_tags = emails_df[emails_df['tags'].isnull() | (~emails_df['tags'].fillna('').str.contains(','))]

    if not emails_without_tags.empty:
        return emails_without_tags.fillna('').reset_index().sample(1).iloc[0].to_dict()
    else:
        return "No new messages"

@tool 
def get_projects() -> Annotated[List[Dict[str, Any]], "the project list"]:
    """Returns the list of projects"""
    projects_df = pd.read_csv(os.path.join(workfolder, "projects.csv"))
    return projects_df.to_dict( orient="records")

@tool
def modify_email(email_id: Annotated[int, "The ID of the email to tag."], 
    tag_string: Annotated[str, "The tag to create."]
    ) -> Annotated[str, "result message"]:
    """ Modifies an email identified by its ID, adding a tag to it."""
    try:
        emails_df = pd.read_csv(os.path.join(workfolder, "emails.csv"), index_col='id')
        tags = emails_df.at[email_id, 'tags'] if pd.notna(emails_df.at[email_id, 'tags']) else ''
        tags = tags.split(',') if len(tags) > 1 else []
        tags.append(tag_string)
        tags = list(set(tags))
        tags = ','.join(tags)
        emails_df.at[email_id, 'tags'] = str(tags)
        emails_df.to_csv(os.path.join(workfolder, "emails.csv"), index=True, index_label='id')
        return f"email {email_id} updated successfully with tag {tag_string}"
    except Exception as e:
        return f"email modifying failed {e}"

@tool
def get_reasons() -> Annotated[List[Dict[str, Any]], "the reasons list"]:
    """Returns the list of reasons for sending an email"""
    email_reasons_df = pd.read_csv(os.path.join(workfolder, "email_reasons.csv"))
    return email_reasons_df.to_dict(orient="records")

tools=[
    to_fastmcp(get_emails), 
    to_fastmcp(get_projects), 
    to_fastmcp(get_reasons), 
    to_fastmcp(modify_email), 
    to_fastmcp(send_email), 
    ]

mcp = FastMCP("mcp", tools=tools)

if __name__ == "__main__":

    print(get_projects.invoke(''))
    print(get_reasons.invoke(''))
    # print('send_email:', send_email.invoke(input={"from_email":"admin@example.com", "to_email":"user@example.com", "subject":"Test Subject", "body":"This is a test email"}))
    # email = get_emails.invoke('')
    # print('get_emails:', email)
    # print('modify_email:', modify_email.invoke(input={"email_id":email['id'], "tag_string":"tag1"}))
    # print('get_emails:', get_emails.invoke(''))
    # print(modify_email.invoke(input={"email_id":email['id'], "tag_string":"tag2"}))
    # print(modify_email.invoke(input={"email_id":email['id'], "tag_string":"tag3"}))

    # mcp.run(transport="stdio")
