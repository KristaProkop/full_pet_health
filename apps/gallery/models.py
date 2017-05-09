# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from ..cphh.models import Client
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor

# Create your models here.
class TestimonialManager(models.Manager):
    def submit_testimonial(self, postData, image, id):
        try:
            client = Client.objects.get(id=id)
            image = Image.objects.create(client=client, model_pic=image, pet_name=postData['pet_name'])
            testimonial = Testimonial.objects.create(client=client, testimonial = postData['testimonial'])
            body = "New gallery submission from {0} {1} awaiting your approval! http://chicagopethealth.com/manage".format(client.first_name, client.last_name)
            email = EmailMessage(
                'CPHH.com New Gallery Submission', 
                body,
                to=['meganacarolan@gmail.com']
            )
            email.send()
            return True
        except:
            return False

class Image(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True)
    model_pic = fields.ImageField(dependencies=[
        FileDependency(processor=ImageProcessor(
            format='PNG', scale={'max_width': 500, 'max_height': 500}))
    ])
    moderated = fields.BooleanField(default=False)
    pet_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Testimonial(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True)
    testimonial = fields.TextField()
    moderated = fields.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TestimonialManager()
