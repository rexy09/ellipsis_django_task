from os import link
from django.db import models
from shortener.models import UrlMap
from datetime import datetime

# Create your models here.


class ShortUrl(models.Model):
    link = models.OneToOneField(
        UrlMap, related_name='short_link', on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)
    
    @property
    def disabled(self):
        if datetime.now() > self.link.date_expired:
            return 'Diable' 
        elif datetime.now() < self.link.date_expired:
            return 'Active'

    class Meta:
        verbose_name = "ShortUrl"
        verbose_name_plural = "ShortUrls"

    def __str__(self):
        return self.link.user.username
