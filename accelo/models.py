from __future__ import unicode_literals

from django.db import models

class Acm(models.Model):
	uid=models.IntegerField(default=0);
	vid=models.IntegerField(default=0);
	pos=models.IntegerField(default=0);
	X= models.FloatField(default=0);
	Y= models.FloatField(default=0);
	Z= models.FloatField(default=0);
	timestamp = models.DateTimeField("Time Stamp");

class Accmeter(models.Model):
	uid=models.IntegerField(default=0);
	vid=models.IntegerField(default=0);
	X= models.FloatField(default=0);
	Y= models.FloatField(default=0);
	Z= models.FloatField(default=0);
	timestamp = models.DateTimeField("Time Stamp");

class Calibrat(models.Model):
	uid=models.IntegerField(default=0);
	vid=models.IntegerField(default=0);
	Sx= models.FloatField(default=1);
	Sy= models.FloatField(default=1);
	Sz= models.FloatField(default=1);
	Ox= models.FloatField(default=0);
	Oy= models.FloatField(default=0);
	Oz= models.FloatField(default=0);
	timestamp = models.DateTimeField("Time Stamp");

class Ace(models.Model):
	uid=models.IntegerField(default=0);
	vpq=models.IntegerField(default=0);
	pos=models.IntegerField(default=0);
	Sz= models.FloatField(default=0);
	Oz= models.FloatField(default=0);
	timestamp = models.DateTimeField("Time Stamp");
