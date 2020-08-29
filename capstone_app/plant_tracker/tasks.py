from __future__ import absolute_import
from twilio.rest import Client

# Twilio API
TWILIO_NUMBER = '+12029533695'
TWILIO_ACCOUNT_SID = 'AC394a9987d3a0e74bbe4f153a27b64434'
TWILIO_AUTH_TOKEN = 'e7645de01db293d8784532a5a34fcdaf'

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

from apscheduler.schedulers.background import BackgroundScheduler
class ReminderScheduler:
    def __init__(self, user, nickname, watering):
        # get user info to schedule SMS reminder
        self.username = user.get_name()
        self.phonenum = user.get_phone()
        self.nickname = nickname
        self.watering = watering

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_executor('processpool')

        self.job = None

    def start_scheduler(self):
        self.job = self.scheduler.add_job(send_sms_reminder, 'interval', args=[self.username, self.nickname, self.phonenum], days=int(self.watering))
        try:
            self.scheduler.start()
            print("Scheduler started")
        except:
            # This shouldn't happen because then the user wouldn't get notifications
            print("Scheduler failed to start")

    def stop_scheduler(self):
        try:
            self.job.remove()
        except:
            print("Unable to remove job/no job currently")

    def edit_scheduler(self, new_day_interval):
        try:
            self.job.modify(days=new_day_interval)
        except:
            print("Unable to remove job/no job currently")

    def delete_scheduler(self):
        self.scheduler.shutdown(wait=False)


