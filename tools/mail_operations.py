
import requests
import json
from typing import Optional, Dict, Any
from datetime import datetime
import msal

class OutlookEmailRetriever:
    """
    A class to retrieve the last email from Outlook 365 using Microsoft Graph API.
    Supports both client credentials and device code authentication flows.
    """

    def __init__(self, client_id: str, client_secret: Optional[str] = None, 
                 tenant_id: Optional[str] = None):
        """
        Initialize the OutlookEmailRetriever.

        Args:
            client_id (str): Azure AD application client ID
            client_secret (str, optional): Client secret for app-only authentication
            tenant_id (str, optional): Tenant ID for app-only authentication
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.access_token = None

    def authenticate_with_device_code(self) -> bool:
        """
        Authenticate using device code flow (delegated permissions).
        This method requires user interaction.

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Create public client application for device code flow
            app = msal.PublicClientApplication(
                client_id=self.client_id,
                authority="https://login.microsoftonline.com/common"
            )

            # Define required scopes
            scopes = ["https://graph.microsoft.com/Mail.Read"]

            # Initiate device flow
            flow = app.initiate_device_flow(scopes=scopes)
            if "user_code" not in flow:
                raise ValueError("Failed to create device flow")

            print(flow["message"])

            # Complete the device flow
            result = app.acquire_token_by_device_flow(flow)

            if "access_token" in result:
                self.access_token = result["access_token"]
                print("Authentication successful!")
                return True
            else:
                print(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
                return False

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return False

    def authenticate_with_client_credentials(self) -> bool:
        """
        Authenticate using client credentials flow (application permissions).
        This method does not require user interaction but needs admin consent.

        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not self.client_secret or not self.tenant_id:
            print("Client secret and tenant ID are required for client credentials flow")
            return False

        try:
            # Create confidential client application
            app = msal.ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=f"https://login.microsoftonline.com/{self.tenant_id}"
            )

            # Acquire token for client
            result = app.acquire_token_for_client(
                scopes=["https://graph.microsoft.com/.default"]
            )

            if "access_token" in result:
                self.access_token = result["access_token"]
                print("Authentication successful!")
                return True
            else:
                print(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
                return False

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return False

    def get_last_email(self, user_email: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve the last (most recent) email from the user's inbox.

        Args:
            user_email (str, optional): Email address of user (required for app-only auth)

        Returns:
            Dict[str, Any]: Email data or None if failed
        """
        if not self.access_token:
            print("Not authenticated. Call authenticate method first.")
            return None

        try:
            # Determine the endpoint based on authentication type
            if user_email:
                # For application permissions, specify the user
                endpoint = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages"
            else:
                # For delegated permissions, use 'me'
                endpoint = "https://graph.microsoft.com/v1.0/me/messages"

            # Set up request parameters
            params = {
                "$top": 1,  # Get only the most recent email
                "$orderby": "receivedDateTime desc",  # Order by most recent first
                "$select": "id,subject,sender,receivedDateTime,bodyPreview,body,toRecipients,hasAttachments"
            }

            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }

            # Make the API request
            response = requests.get(endpoint, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()

                if data.get("value") and len(data["value"]) > 0:
                    email = data["value"][0]  # Get the first (most recent) email
                    return self._format_email_data(email)
                else:
                    print("No emails found in inbox.")
                    return None

            else:
                print(f"Failed to retrieve emails. Status code: {response.status_code}")
                print(f"Error: {response.text}")
                return None

        except Exception as e:
            print(f"Error retrieving email: {str(e)}")
            return None

    def _format_email_data(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format email data for better readability.

        Args:
            email (Dict[str, Any]): Raw email data from Graph API

        Returns:
            Dict[str, Any]: Formatted email data
        """
        # Extract sender information
        sender_info = email.get("sender", {})
        sender_email = sender_info.get("emailAddress", {})

        # Extract recipients
        recipients = []
        for recipient in email.get("toRecipients", []):
            recipient_email = recipient.get("emailAddress", {})
            recipients.append({
                "name": recipient_email.get("name", ""),
                "address": recipient_email.get("address", "")
            })

        # Format the email data
        formatted_email = {
            "id": email.get("id"),
            "subject": email.get("subject", "No Subject"),
            "sender": {
                "name": sender_email.get("name", "Unknown"),
                "address": sender_email.get("address", "Unknown")
            },
            "recipients": recipients,
            "received_datetime": email.get("receivedDateTime"),
            "body_preview": email.get("bodyPreview", ""),
            "body_content": email.get("body", {}).get("content", ""),
            "body_content_type": email.get("body", {}).get("contentType", ""),
            "has_attachments": email.get("hasAttachments", False)
        }

        return formatted_email

    def print_email_summary(self, email: Dict[str, Any]) -> None:
        """
        Print a formatted summary of the email.

        Args:
            email (Dict[str, Any]): Formatted email data
        """
        print("\n" + "="*60)
        print("LAST EMAIL SUMMARY")
        print("="*60)
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender']['name']} <{email['sender']['address']}>")

        if email['recipients']:
            recipients_str = ", ".join([f"{r['name']} <{r['address']}>" for r in email['recipients']])
            print(f"To: {recipients_str}")

        # Parse and format the received datetime
        try:
            dt = datetime.fromisoformat(email['received_datetime'].replace('Z', '+00:00'))
            formatted_dt = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"Received: {formatted_dt}")
        except:
            print(f"Received: {email['received_datetime']}")

        print(f"Has Attachments: {'Yes' if email['has_attachments'] else 'No'}")
        print(f"Body Preview: {email['body_preview'][:100]}...")
        print("="*60)


# Example usage functions
def example_with_device_code():
    """
    Example using device code authentication (requires user interaction)
    """
    # Replace with your registered app's client ID
    client_id = "your-client-id-here"

    # Create retriever instance
    retriever = OutlookEmailRetriever(client_id)

    # Authenticate with device code flow
    if retriever.authenticate_with_device_code():
        # Get the last email
        last_email = retriever.get_last_email()

        if last_email:
            retriever.print_email_summary(last_email)
            return last_email
        else:
            print("Could not retrieve the last email.")
    else:
        print("Authentication failed.")

    return None

def example_with_client_credentials():
    """
    Example using client credentials authentication (app-only)
    """
    # Replace with your registered app's details
    client_id = "your-client-id-here"
    client_secret = "your-client-secret-here"
    tenant_id = "your-tenant-id-here"
    user_email = "user@yourdomain.com"  # Email of the user whose mailbox to access

    # Create retriever instance
    retriever = OutlookEmailRetriever(client_id, client_secret, tenant_id)

    # Authenticate with client credentials flow
    if retriever.authenticate_with_client_credentials():
        # Get the last email for the specified user
        last_email = retriever.get_last_email(user_email)

        if last_email:
            retriever.print_email_summary(last_email)
            return last_email
        else:
            print("Could not retrieve the last email.")
    else:
        print("Authentication failed.")

    return None

# Simple function version for quick usage
def get_last_email_simple(client_id: str, client_secret: str = None, 
                         tenant_id: str = None, user_email: str = None) -> Optional[Dict[str, Any]]:
    """
    Simple function to get the last email from Outlook 365.

    Args:
        client_id (str): Azure AD application client ID
        client_secret (str, optional): Client secret for app-only auth
        tenant_id (str, optional): Tenant ID for app-only auth  
        user_email (str, optional): User email for app-only auth

    Returns:
        Dict[str, Any]: Last email data or None if failed
    """
    retriever = OutlookEmailRetriever(client_id, client_secret, tenant_id)

    # Choose authentication method based on provided parameters
    if client_secret and tenant_id:
        auth_success = retriever.authenticate_with_client_credentials()
    else:
        auth_success = retriever.authenticate_with_device_code()

    if auth_success:
        return retriever.get_last_email(user_email)
    else:
        return None

if __name__ == "__main__":
    # Example usage
    print("Choose authentication method:")
    print("1. Device Code Flow (requires user interaction)")
    print("2. Client Credentials Flow (app-only, requires admin consent)")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        example_with_device_code()
    elif choice == "2":
        example_with_client_credentials()
    else:
        print("Invalid choice. Please run again and select 1 or 2.")
