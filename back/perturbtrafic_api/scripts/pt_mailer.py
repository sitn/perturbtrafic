from pyramid_mailer.message import Message
from pyramid.renderers import render
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
import premailer

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

import logging
log = logging.getLogger(__name__)


class PTMailer():

    @classmethod
    def send_mail(cls, request, recipients, subject, body):
        try:
            mailer = request.registry['mailer']
            message = Message(subject=subject,
                              sender=request.registry.settings['mail.username'],
                              recipients=recipients,
                              body=body)

            mailer.send_immediately(message, fail_silently=False)
        except Exception as error:
            raise error

        return True


    @classmethod
    def send_templated_mail_old(cls, request, recipients, subject, template, context, dynamic_content=None):
        try:
            assert recipients
            assert len(recipients) > 0
            mailer = request.registry['mailer']

            html_body = render(template + ".body.pt", context, request=request)
            #text_body = render(template + ".body.txt", context, request=request)

            # Inline CSS styles
            html_body = premailer.transform(html_body)

            if dynamic_content:
                html_body = html_body.replace('@@dynamic_content@@', dynamic_content)
            elif dynamic_content == None or dynamic_content == '':
                html_body = html_body.replace('<tr>@@dynamic_content@@</tr>', '')

            message = Message(subject=subject,
                              sender=request.registry.settings['mail.username'],
                              recipients=recipients,
                              html=html_body)

            mailer.send_immediately(message, fail_silently=False)

        except Exception as error:
            raise error

        return True\

    @classmethod
    def send_templated_mail(cls, request, recipients, subject, template, context, dynamic_content=None):
        try:
            host = request.registry.settings['mail.host']
            port = request.registry.settings['mail.port'] if 'mail.port' in request.registry.settings else None
            user = request.registry.settings['mail.username']
            pwd = request.registry.settings['mail.password'] if 'mail.password' in request.registry.settings else None

            msg = MIMEMultipart()
            msg['From'] = user
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject
            html_body = render(template + ".body.pt", context, request=request)

            # Inline CSS styles
            html_body = premailer.transform(html_body)

            if dynamic_content:
                html_body = html_body.replace('@@dynamic_content@@', dynamic_content)
            elif dynamic_content == None or dynamic_content == '':
                html_body = html_body.replace('@@dynamic_content@@', '')

            body = html_body

            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP(host, port if port else None)
            server.ehlo()
            server.starttls()
            server.ehlo()

            if user and pwd:
                server.login(user, pwd)

            text = msg.as_string()
            server.sendmail(user, recipients, text)

            server.quit()

        except Exception as error:
            raise error