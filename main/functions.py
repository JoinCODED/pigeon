from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
import nexmo


def sendEmail(recipient,subject,message):
    context = {
        'recipient': recipient
    }
    html_content = render_to_string(message, context=context)
    text_content = strip_tags(html_content)
    send_mail(subject, text_content, settings.EMAIL_HOST_USER , [recipient.email,], fail_silently=True, html_message=html_content)


def sendSms(recipient,message):
    client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
    client.send_message({
        'from': 'Pigeon',
        'to': str(recipient.number),
        'text': message
        })

    
