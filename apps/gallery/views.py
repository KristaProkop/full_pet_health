# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings

from ..cphh.models import Client
from .models import Image, Testimonial
from .forms import ImageUploadForm


    
def gallery(request):
    if request.method == 'POST':  
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            success = Testimonial.objects.submit_testimonial(request.POST, form.cleaned_data['image'], request.session['id'])
            if success:
                messages.success(request, "Success! Your submission is under review.")
        else:
            messages.error(request, "Something went wrong :( Try again? Please fill out all fields and include a pic!")
        return redirect(reverse('gallery:gallery'))
    else:
        context = {
            'images': Image.objects.filter(moderated=True).order_by('-created_at'),
            'testimonials': Testimonial.objects.filter(moderated=True).order_by('-created_at'),
            'media_url': settings.MEDIA_URL,
        }
        #Only display first letter of last name in gallery
        for testimonial in context['testimonials']:
            testimonial.client.last_name_initial =  testimonial.client.last_name[0]
        return render(request,'gallery/gallery.html', context)


def destroy_image(request, id):
    if request.session['email'] == settings.ADMIN_EMAIL:
        image = Image.objects.get(id=id).delete()
    return redirect(reverse('gallery:manage'))
    
def approve_image(request, id):
    if request.session['email'] == settings.ADMIN_EMAIL:
        image = Image.objects.get(id=id)
        image.moderated = True
        image.save()
    return redirect(reverse('gallery:manage'))

def destroy_testimonial(request, id):
    if request.session['email'] == settings.ADMIN_EMAIL:
        testimonial = Testimonial.objects.get(id=id).delete()
    return redirect(reverse('gallery:manage'))

def approve_testimonial(request, id):
    if request.session['email'] == settings.ADMIN_EMAIL:
        testimonial = Testimonial.objects.get(id=id)
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
