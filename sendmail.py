import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_noti_email(content:str):
    #The mail addresses and password
    sender_address = "fusionnotifier@gmail.com"
    sender_pass = "fcfsnbmwyfswlhks"
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    receiver_addresses = open("receivers.txt", "r").read().splitlines()
    message['To']=", ".join(receiver_addresses)
    message['Subject'] = 'THERE MIGHT BE AVAILABLE TICKETS!'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()

    session.sendmail(sender_address, receiver_addresses, text)
    session.quit()
