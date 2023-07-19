import requests
import os


import os
"""
 * Send an email message by using Infobip API.
 *
 * This example is already pre-populated with your account data:
 * 1. Your account Base URL
 * 2. Your account API key
 * 3. Your recipient email
 *
 * THIS CODE EXAMPLE IS READY BY DEFAULT. HIT RUN TO SEND THE MESSAGE!
 *
 * Send email API reference: https://www.infobip.com/docs/api#channels/email/send-email
 * See Readme file for details.
"""

BASE_URL = "https://2k2m16.api.infobip.com"
API_KEY = "App 14dac9e117343afd7b60c23bc999a425-b9475ccb-06b4-4587-a8fa-54d15cd498ad"

SENDER_EMAIL = "klick123@selfserviceib.com"
RECIPIENT_EMAIL = "andrewskvarcius@gmail.com"
EMAIL_SUBJECT = "This is a sample email subject"
EMAIL_TEXT = "This is a sample email message."

BASE_FILE_PATH = "/home/infobip/project/src/email/files"

file_name = "infobip.png"

file = open(os.path.join(BASE_FILE_PATH, file_name), 'rb')
files = {'attachment': (file_name, file)}

form_data = {
    "from": SENDER_EMAIL,
    "to": RECIPIENT_EMAIL,
    "subject": EMAIL_SUBJECT,
    "text": EMAIL_TEXT
}

all_headers = {
    "Authorization": API_KEY
}

response = requests.post(BASE_URL + "/email/3/send", data=form_data, files=files, headers=all_headers)

file.close()

print("Status Code: " + str(response.status_code))
print(response.json())
