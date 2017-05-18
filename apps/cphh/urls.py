from django.conf.urls import url

from . import views
from .views import LoginView

urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^$', views.index, name="index"),
    url(r'^contact$', views.contact, name="contact"),
    url(r'^register$', views.register, name="register"),
    url(r'^logout$', views.logout, name="logout"),  
]