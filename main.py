import csv
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

USERNAME = 'f74bc135d638ab'
PASSWORD = 'a803e3de54bf20'


def create_mail(user, template):
    message = template.substitute(PERSON_NAME=user['Name'].title())
    subject = "An email from Python"
    msg = MIMEMultipart()
    msg["From"] = USERNAME
    msg["To"] = user['Email']
    msg["Subject"] = subject
    msg.attach(MIMEText(message, 'plain'))
    return msg


def read_template():
    with open('message.txt', 'r', encoding='utf-8') as template_file:
        template_file = template_file.read()
    return Template(template_file)


def login_server():
    server = smtplib.SMTP('smtp.mailtrap.io', 2525)
    server.ehlo()
    server.starttls()
    server.login(USERNAME, PASSWORD)
    return server


def read_send_mail(message_template):
    with open("contacts.csv", "r") as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        server = login_server()
        count = 0
        print('Sending...')
        for row in data:
            t1 = time.time()
            name, email = row[0].split(',')
            user = {'Name': name, 'Email': email}
            msg = create_mail(user, message_template)
            # server.sendmail(msg.get('From'), msg["To"], msg.as_string())
            count += 1
            del msg
            time.sleep(0.5)
            print(f"{count}, {time.time() - t1} seconds")
        server.close()
        print('successfully Finished')


def main():
    message_template = read_template()
    read_send_mail(message_template)


if __name__ == "__main__":
    main()