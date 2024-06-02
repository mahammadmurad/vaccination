from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from user.utils import EmailVerificationTokenGenerator
from django.contrib.auth import get_user_model

User = get_user_model()

def send_email_verification(request, pk):
    user = User.objects.get(pk=pk)
    current_site = get_current_site(request)
    subject = 'Request for email verification'
    message  = render_to_string(
        template_name= 'user/email_verification.html',
        context={
            'full_name': user.get_full_name(),
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': EmailVerificationTokenGenerator.make_token(user)
        }
    )
    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    return email.send()