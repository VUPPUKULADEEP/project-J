import smtplib
from email.message import EmailMessage


def send_email():
    email ="vuppukuladeep@gmail.com" 
    reciever = 'a60794567@gmail.com'
    subject = 'sample'
    message = 'techfest 2k24'
    text = f'subject : {subject}\n\n  {message}'
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email,"ovbu muyi ijnp tvhg")
    server.sendmail(email,reciever,text)
    print('email send')

send_email()