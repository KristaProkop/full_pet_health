# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views import View

from .models import Client, Inquiry, Message

class LoginView(View):
    def get(self, request):
        return render(request,'cphh/login.html')

    def post(self, request):
        login_valid, login_response = Client.objects.login(request.POST)
        if login_valid:
            request.session['id'] = login_response.id
            request.session['email'] = login_response.email
            if request.session['email'] ==settings.ADMIN_EMAIL:
                return redirect(reverse('gallery:manage'))
            else:
                return redirect(reverse('gallery:gallery'))
        else:
            messages.error(request, login_response)


def index(request):
    return render(request, 'cphh/index.html')

def contact(request):
    if request.method == 'POST':
        try:
            inquiry_id = Inquiry.objects.create_inquiry(request.POST)
            message = Message.objects.create_message(request.POST)
            contact_success = Inquiry.objects.send_email(request.POST)
            if contact_success:
                messages.success(request, "Successfully sent! We will respond within 1 business day.")
        except: 
            messages.error(request, "Something went wrong. Please try again or call us during normal business hours.")
    return redirect(reverse('cphh:index'))
    

def register(request):
    if request.method == "POST":
        reg_valid, reg_response = Client.objects.validate(request.POST)
        if reg_valid:
            login_valid, login_response = Client.objects.login(request.POST)
            if login_valid:
                request.session['id'] =login_response.id
                messages.success(request, "Successfully registered!")
                return redirect(reverse('gallery:gallery'))
            else: 
                messages.error(request, login_response)
        else: 
            messages.error(request, reg_response)
    return render(request,'cphh/login.html')

def logout(request):
    request.session.clear()
    return redirect(reverse('cphh:index'))
