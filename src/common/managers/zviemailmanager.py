import subprocess

from src.constants.zviconstants import constants

if constants.system == "Windows":
    import win32com.client as win32


class EmailManager:
    def __init__(self):
        if constants.system == "Windows":
            self.outlook = win32.Dispatch('outlook.application')

    def sendHTMLEmail(self, email, subject, body):
        mail = self.outlook.CreateItem(0)
        mail.To = email
        mail.Subject = subject
        mail.HTMLBody = body
        mail.Send()

    def sendEmail(self, to, subject, body, attachment=None):
        if constants.system == "Windows":
            mail = self.outlook.CreateItem(0)
            mail.To = to
            mail.Subject = subject
            mail.Body = body
            if attachment:
                mail.Attachments.Add(Source=attachment)
            mail.Send()
        else:
            subprocess.Popen(['xdg-email', "--subject '{0}'".format(subject),
                              "--body '{0}'".format(body), to])
