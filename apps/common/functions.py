#coding: utf-8
import logging
from django.utils.translation import ugettext_lazy as _
from apps.common.models import Message_Type
from apps.customer.models import Notification
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

def handle_uploaded_file(files, tempDir, name, min_size):
    from PIL import Image
    img = files[0]
    file_type = img.content_type.split('/')[1] if img.content_type != '' else ''
    if file_type not in ('png', 'jpeg', 'jpg', ''):
        return ('You should upload an image file')

    #Check image type
    try:
        tempFile = Image.open(img)
        size = tempFile.size
        if size[0] < min_size or size[1] < min_size:
            return ('Upload image file size should be at least 200x200')

    except Exception, error:
        logging.exception(error)
        return ('System error')

    f = tempDir + name + '.png'
    f = f.encode('ascii', 'ignore')
    destination = open(f, 'wb+')
    for chunk in img.chunks():
        destination.write(chunk)
    destination.close()

    img = Image.open(f)
    img.thumbnail( (400, 400), Image.ANTIALIAS)
    img.save(f, "JPEG", quality=80, optimize=True, progressive=True)

    tempFile.save(tempDir + name + '_original' + '.png')
    return ''


def send_email(email_from, email_to, subject, html_content):
    try:
        msg = EmailMessage(subject, html_content, email_from, [email_to])
        msg.content_subtype = "html"
        msg.send()
    except Exception, ex:
        logging.exception(ex)
        return False
    return True


def send_message(recipient_id, sender_id=None, subject='', body_html='', object_id=None, type=Message_Type._MESSAGE_NORMAL, notify=True, sendmail=False, mobile=False):
    if notify:
        Notification(recipient_id=recipient_id, sender_id=sender_id, subject=subject,
                     body=body_html, object_id=object_id, type=type).save()

    if sendmail:
        full_name = 'Demo-Oscar'
        email_from = full_name + ' <demo@oscar.com>'
        if sender_id:
            sender = User.objects.filter(id=sender_id)[0]
            full_name = sender.get_full_name()
            email_from = full_name + ' <' + sender.email + '>'

        recipient = User.objects.filter(id=recipient_id)[0]
        email_to = recipient.email

        send_email(email_from, email_to, subject, body_html)









