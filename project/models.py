import random
import string
from django.db import models
import django.utils.timezone as tz
from datetime import datetime, timedelta
import django.db.models.signals as signals
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

def create_user_profile(sender, instance, created, **kwargs):
	if created: Profile.objects.create(user=instance)
signals.post_save.connect(create_user_profile, sender=User, weak=False, dispatch_uid='models.create_user_profile')

class Entry(models.Model):
	server_name = models.CharField(max_length=1000)
	server_ip = models.CharField(max_length=100)
	message = models.CharField(max_length=10000)

def a_time_in_the_future():
	return tz.now() + timedelta(minutes=20)

def random_password():
	return "".join([random.choice(string.digits + string.letters) for i in range(4)]).lower()

class Reservation(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	time = models.DateTimeField(default=tz.now)
	expiration = models.DateTimeField(default=a_time_in_the_future)
	password = models.CharField(max_length=100, default=random_password)
	map = models.CharField(max_length=100)
	
	@staticmethod
	def current():
	 	return Reservation.objects.filter(expiration__gt=tz.now()).last()
