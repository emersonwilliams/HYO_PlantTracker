from __future__ import absolute_import
from twilio.rest import Client

# Twilio API
TWILIO_NUMBER = '+12029533695'
TWILIO_ACCOUNT_SID = 'AC394a9987d3a0e74bbe4f153a27b64434'
TWILIO_AUTH_TOKEN = '47b1578be926ded81995c5582057a774'

# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms_reminder(username, nickname, phonenum):
    """Send a reminder to a phone using Twilio SMS"""

    body = 'Hi {0}! Remember to water {1} today!'.format(
        username,
        nickname
    )

    client.messages.create(
        body=body,
        to="+1"+phonenum,
        from_=TWILIO_NUMBER,
    )