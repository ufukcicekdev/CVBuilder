from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.db.models import F
from collections import defaultdict
from django.template.loader import render_to_string
import os
from dotenv import load_dotenv
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.models import User
from profiles.models import GeneratedCV
from translateContext.translateContext import *


EMAIL_HOST_USER = "info@cvbuilder.tech"

def check_generated_cv():
    users_without_cv = User.objects.filter(is_superuser=False).exclude(id__in=GeneratedCV.objects.values_list('user_id', flat=True))
    for user in users_without_cv:
        send_generated_reminder_email(user)

def send_generated_reminder_email(user):
    current_lang = Profile.objects.filter(user_id=user.id).first()
    mail_context = get_trans_lang_1(current_lang.language)
    subject = mail_context.get("profile_update_mail_title")
    email_temp = mail_context.get('profile_update_mail_content')
    email_content = email_temp.format(username=user.username)
    mail_context["profile_update_mail_content"] = email_content
    email_content = render_to_string('email_templates/profileUpdate.html', mail_context)
    email = EmailMessage(subject, email_content, EMAIL_HOST_USER, to=[user.email])
    email.content_subtype = 'html'
    email.send()




def update_cv():
    users_with_cv = User.objects.filter(id__in=GeneratedCV.objects.values_list('user_id', flat=True))
    for user in users_with_cv:
        send_update_reminder_email(user)

def send_update_reminder_email(user):
    current_lang = Profile.objects.filter(user_id=user.id).first()
    mail_context = get_trans_lang_1(current_lang.language)
    subject = mail_context.get("profile_update_mail_title")
    email_temp = mail_context.get('profile_update_mail_content1')
    email_content = email_temp.format(username=user.username)
    mail_context["profile_update_mail_content"] = email_content
    email_content = render_to_string('email_templates/profileUpdate.html', mail_context)
    email = EmailMessage(subject, email_content, EMAIL_HOST_USER, to=[user.email])
    email.content_subtype = 'html'
    email.send()