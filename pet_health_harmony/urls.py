
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from apps.cphh.models import Client, Message, Inquiry
from apps.gallery.models import Image, Testimonial


class ClientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Client, ClientAdmin)

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)

class InquiryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Inquiry, InquiryAdmin)

class ImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Image, ImageAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    pass
admin.site.register(Testimonial, TestimonialAdmin)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.cphh.urls', namespace='cphh')),
    url(r'^', include('apps.gallery.urls', namespace='gallery')),

]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)