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
			try:
				message = f"Dear {link.link.user.username}, as short URL: {link.link.short_url} for {link.link.full_url} has expired."

				send_mail(subject="SHORT URL EXPIRED", message=message,
                                    recipient_list=[link.link.user.profile.email], from_email='admin@test.com')
			except Exception as e:
				print(e)
				pass
			
			
			link.expired = True
			link.save()
	else:
		pass


