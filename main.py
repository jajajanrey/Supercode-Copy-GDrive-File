""" Import required libraries """
import os
import json

from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = '/tmp/credentials.json'


def get_credentials(credentials):
    """
        We have to write it to a file because gcs
        library only accepts a file path.
    """
    with open(CREDENTIALS_PATH, "w") as credentials_file:
        credentials_file.write(credentials)

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPES)

    return credentials


def main(file_id, service_account_json, title="", user_email=""):
    """ Copy a file from google drive. """

    credentials = get_credentials(service_account_json)
    service = build('drive', 'v3', credentials=credentials)

    copy = {
        "name": title,
        "title": title
    }

    try:
        copy = service.files().copy(fileId=file_id, body=copy).execute()
        if copy:
            if user_email:
                permissions = {
                    'type': 'user',
                    'role': 'writer',
                    'emailAddress': user_email
                }

                req = service.permissions().create(
                    fileId=copy.get("id"),
                    body=permissions,
                    fields="id"
                )

            req.execute()

            copy["success"] = True
            copy["description"] = "Successfully copied file from google drive."

    except Exception:
        copy["success"] = False
        copy["description"] = "There is a problem with the Google Drive API, please try again."

    return copy
