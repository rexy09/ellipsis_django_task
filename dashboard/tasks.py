from django.core.mail import send_mail
from celery import shared_task
from .models import *
# DateTime
from datetime import datetime
from django.conf import settings

# Create your tasks here


@shared_task
def send_url_expire_email_notification(*args, **kwargs):
	datetime_now = datetime.now()

	links = ShortUrl.objects.filter(
		expired=False, link__date_expired__lte=datetime_now).all()

	if links:
		for link in links:
			message = f"Dear {link.user.username}, as short URL: {link.short_url} for {link.full_url} has expired."

			send_mail(subject="SHORT URL EXPIRED", message=message,
			          recipient_list=[link.user.profile.email],)
			
			link.expired = True
			link.save()
	else:
		pass


