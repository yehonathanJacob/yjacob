import json
from threading import Thread, Event
import sendgrid
from queue import Queue
from datetime import datetime
from dateutil import tz
import logging
import platform

work_queue = Queue()


def email_worker(api_key, stop_event):
    while not stop_event.is_set():
        item = work_queue.get()

        try:
            sg = sendgrid.SendGridAPIClient(apikey=api_key)
            sg.client.mail.send.post(request_body=item)
        except:
            logging.exception('Error sending mail')

        work_queue.task_done()


class MailSender(object):

    def __init__(self, api_key, admin_emails):
        self.api_key = api_key
        self.admin_emails = admin_emails
        self.worker_thread = None
        self.stop_worker_event = None
        self.hostname = None

    def init(self):
        if not self.api_key or not self.admin_emails:
            return

        self.stop_worker_event = Event()
        self.worker_thread = Thread(target=email_worker, args=(self.api_key, self.stop_worker_event))
        self.worker_thread.daemon = True
        self.worker_thread.start()
        self.hostname = platform.uname()[1]

    def send_login_email(self, user):
        if not self.api_key or not self.admin_emails:
            return

        il_tz = tz.gettz('Israel')
        il_datetime = datetime.now().replace(tzinfo=il_tz)

        subject = user.username + ' logged in at ' + il_datetime.strftime('%d/%m/%Y %H:%M:%S') + ' to ' + self.hostname
        data = self._prepare_email_data(subject, subject, self.admin_emails)

        work_queue.put(data)

    def send_new_user_credentials_and_report_email(self, new_user_dict, report=None):
        if not self.api_key:
            return
        subject = 'New profile: {name} created on host: {hostname}'.format(
            name=new_user_dict.get('username'),
            hostname=self.hostname
        )
        body = 'Username: {username}\n\nPassword: {password}\n\n'.format(
            username=new_user_dict.get('username'),
            password=new_user_dict.get('password'),
        )
        if report:
            body += '\n\nUser data import report: \n{}'.format(json.dumps(report))

        data = self._prepare_email_data(subject, body, new_user_dict.get('email'))
        work_queue.put(data)

    def send_support_email(self, user, description, study_uid=None):
        if not self.api_key or not self.admin_emails:
            return

        il_tz = tz.gettz('Israel')
        il_datetime = datetime.now().replace(tzinfo=il_tz)

        subject = user.username + ' requested support at ' + il_datetime.strftime('%d/%m/%Y %H:%M:%S')
        body = 'Problem description: ' + description
        if study_uid:
            body += '\n\nStudy uid: ' + study_uid

        data = self._prepare_email_data(subject, body, self.admin_emails)

        work_queue.put(data)

    def _prepare_email_data(self, subject, body, recipients, type='text/plain'):
        return {
            'personalizations': [
                {
                    'to': [{'email': email} for email in list(recipients)],
                    'subject': subject
                }
            ],
            'from': {
                'email': 'admin@aidoc.com',
                'name': 'Aidoc Admin'
            },
            'content': [
                {
                    'type': type,
                    'value': body
                }
            ]
        }

    def destroy(self):
        if self.worker_thread:
            self.stop_worker_event.set()
            self.worker_thread = None
