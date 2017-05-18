# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views import View

from ..cphh.models import Client
from .models import Image, Testimonial
from .forms import ImageUploadForm

class GalleryView(View):
    def get(self, request):
        context = {
            'images': Image.objects.filter(moderated=True).order_by('-created_at'),
            'testimonials': Testimonial.objects.filter(moderated=True).order_by('-created_at'),
            'media_url': settings.MEDIA_URL,
        }
        #Only display first letter of last name in gallery
        for testimonial in context['testimonials']:
            testimonial.client.last_name_initial =  testimonial.client.last_name[0]
        return render(request,'gallery/gallery.html', context)

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            success = Testimonial.objects.submit_testimonial(request.POST, form.cleaned_data['image'], request.session['id'])
            if success:
                messages.success(request, "Success! Your submission is under review.")
        else:
            messages.error(request, "Something went wrong :( Try again? Please fill out all fields and include a pic!")
        return redirect(reverse('gallery:gallery'))
    

class ManageImagesView(View):
    def get(self, request, manage_type, id):
        if request.session['email'] != settings.ADMIN_EMAIL:
            return redirect(reverse('gallery:gallery'))
        else:
            image = Image.objects.get(id=id)
            if manage_type == 'destroy':
                image.delete()
            if manage_type == "approve":
                image.moderated = True
                image.save()
            return redirect(reverse('gallery:manage'))

class ManageTestimonialsView(View):
    def get(self, request, manage_type, id):
        if request.session['email'] != settings.ADMIN_EMAIL:
            return redirect(reverse('gallery:gallery'))
        else:
            testimonial = Testimonial.objects.get(id=id)
            if manage_type == 'destroy':
                testimonial.delete()
            if manage_type == "approve":
                testimonial.moderated = True
                testimonial.save()
            return redirect(reverse('gallery:manage'))


def manage(request):
    if 'email' not in request.session or request.session['email'] != settings.ADMIN_EMAIL:
        return redirect(reverse('cphh:login'))
    elif request.session['email'] == settings.ADMIN_EMAIL:
        context = {
            'images': Image.objects.all().order_by('moderated'),
            'testimonials': Testimonial.objects.all().order_by('-created_at'),
            'clients': Client.objects.all().order_by('-created_at'),
            'media_url': settings.MEDIA_URL,
        }
        return render(request, 'gallery/manage.html', context) 
