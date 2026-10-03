from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('doctors/', include('doctors.urls')),
    path('specializations/',include('specializations.urls')),
    path('appointments/', include('appointments.urls')),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('',views.home,name='home'),
    path('ai/', include('ai_assistant.urls')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )