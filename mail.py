import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self, receiver):
        self.ctx = ssl.create_default_context()
        self.password = 'rugr rvxy ckfo qmln'    # Your app password goes here
        self.sender = 'pythondiscordbot88@gmail.com'    # Your e-mail address
        self.receiver = receiver # Recipient's address

    def createHeaders(self, subject):
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = subject
        self.message["From"] = "PyDiscord Bot" 
        self.message["To"] = self.receiver

    #order is server invite link, dashboard link (wrapped of course)
    def createBody(self, invite_link, dashboard_link):
        self.html = """\
        <html>
            <body>
                <p>Hello Whoever You Are!</p>
                <br>
                <p>You asked for an invitation link to Python Bot Test Discord server. This invitation has one use, just for you! It will expire within 24 hours, so please use it now with this link: {}</p>
                <br>
                <p>Once you accept the invitation, please go to the site dashboard <span><a href='{}' target='_blank'>here</span> and register your Discord username and hashtag discriminator, along with all other details.
                This usually looks like "username#1234", and you can see it on your profile within the Discord app.
                If you don't register within 12 hours after accepting the invitation, the system will kick you out from the Discord server automatically and you would have to start the process again.
                Once you complete the questions on the dashboard, the system will automatically assign you to the different Discord chat channels based on your choices, so pick wisely :).</p></span>
                <br>
                <br>
                <p>See you on Discord,<p>
                <p>PyDiscord Bot<p>
            </body>
        </html>
        """.format(invite_link, dashboard_link)

    def sendMessage(self):
        self.message.attach(MIMEText(self.html, "html"))

        # Connect with server and send the message
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=self.ctx) as server:
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, self.message.as_string())
