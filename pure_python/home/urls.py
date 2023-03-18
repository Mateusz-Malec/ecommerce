from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('desktops/', views.desktops_, name='desktops'),
                  path('desktops/<c_id>', views.desktop_detail)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
