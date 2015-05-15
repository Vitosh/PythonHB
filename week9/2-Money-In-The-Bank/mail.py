import smtplib
from email.mime.text import MIMEText

username = "Gosho Ivanov"
password = "!@#@#!#@!@#!SGDASFDAFDSAADFS@#@$#SDAADSsfdafsda"
SMTP_USERNAME = "jobanana500@yahoo.com"
SMTP_PASSWORD = "" #no password for you! :P

SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
EMAIL_FROM = SMTP_USERNAME
EMAIL_TO = "jobanana500@yahoo.com"
EMAIL_SUBJECT = "Password reset Money-In-The-Bank Project"
co_msg = """
Hello, {}!
You have requested a password reset.
Please, go to function "reset password" and enter the following password for password: {}.

Have a great day!

Best Regards,

Money-In-The-Bank Team
http://www.vitoshacademy.com

""".format(username, password)


def send_email():
    msg = MIMEText(co_msg)
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    debuglevel = False
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    print("A new mail has been generated and sent to {}.".format(EMAIL_TO))
    mail.quit()

if __name__ == '__main__':
    send_email()
