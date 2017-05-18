from django.conf.urls import url

from . import views
from .views import GalleryView, ManageImagesView, ManageTestimonialsView

urlpatterns = [ 
    url(r'^manage$', views.manage, name='manage'),

    url(r'^gallery$', GalleryView.as_view(), name="gallery"), 
    url(r'^image/(?P<manage_type>[a-zA-Z]+)/(?P<id>\d+)$', ManageImagesView.as_view(), name="manage_image"),
    url(r'^testimonial/(?P<manage_type>[a-zA-Z]+)/(?P<id>\d+)$', ManageTestimonialsView.as_view(), name="manage_testimonial"),
      
]