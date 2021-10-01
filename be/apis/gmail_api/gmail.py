import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from be.apis.gmail_api.google import Create_Service

API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = 'https://mail.google.com/'

english_psychologist_name_to_hebrew = {'leat har-tov': 'ליאת הר-טוב',
                                       'rina aaluf': 'רינה אאלוף',
                                       'clara moldan': 'קלרה מולדן',
                                       'adi grin': 'אדי גרין'}


class GmailAPI:
    def __init__(self):
        self.service = Create_Service(API_NAME, API_VERSION, [SCOPES])

    def send_mail(self, zoom_link, receiver_addresses, date, time, psychologist_name):
        psychologist_name = english_psychologist_name_to_hebrew[psychologist_name]
        emailMsg = "אנונימי, שלום :) \n" \
                       "\n קבעת פגישת זום עם {} בתאריך: {} בשעה: {}" \
                       "\n חשוב לנו להדגיש כי הזום הינו אנונימי והמצלמות כבויות במצב הדיפולטי." \
                       "\n{}".format(psychologist_name, date, time, zoom_link)

        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = receiver_addresses
        mimeMessage['subject'] = 'אנונימי'

        mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        message = self.service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(message)
