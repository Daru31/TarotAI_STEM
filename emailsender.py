import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email.header import Header 
from email import encoders 

class EmailSender: 

    def __init__(self, sender_email, password): 
        self.sender_email = sender_email 
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.port = 587 

    def send_email(self, receiver_email, subject, body, filename): 
        message = MIMEMultipart() 
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain")) 

        with open(filename,"rb") as attachment: # rb = 읽기 전용
            part = MIMEBase("application", "octet_stream") 
            part.set_payload(attachment.read()) 
            encoders.encode_base64(part) 
            filename_encoded = Header(filename, "utf-8").encode() 

            part.add_header(
                "Content_Disposition", f"attachment; filename = {filename_encoded} "
            )
            message.attach(part) 
        with smtplib.SMTP(self.smtp_server, self.port) as server: 
            server.starttls() 
            server.login(self.sender_email, self.password)  
            text = message.as_string() 
            server.sendmail(self.sender_email, receiver_email, text) 

        # print("Debug: Email Sent Successfully!") 

        

        