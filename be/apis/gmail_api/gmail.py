import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailAPI:
    def __init__(self):
        self.sender_address = 'anonymousmtaworkshop@gmail.com'
        self.sender_pass = 'QAZqaz123'

    def send_mail(self, zoom_link, receiver_addresses, date, time):
        mail_content = "אנונימי, שלום :) \n" \
                       "\n קבעת פגישת זום איתנו בתאריך: %s בשעה: %s" \
                       "\n חשוב לנו להדגיש כי הזום הינו אנונימי והמצלמות כבויות במצב הדיפולטי." \
                       "%s".format(date, time, zoom_link)

        message = MIMEMultipart()
        message['From'] = self.sender_address
        message['To'] = ", ".join(receiver_addresses)
        message['Subject'] = 'אנונימי'

        # #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port 587
        session.starttls() #enable security
        session.login(self.sender_address, self.sender_pass) #login with mail_id and password

        text = message.as_string()
        session.sendmail(self.sender_address, receiver_addresses, text)
        session.quit()
        print('Mail Sent')