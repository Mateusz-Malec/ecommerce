from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('computers/', views.computers_, name='computers'),
                  path('computers/<c_id>', views.computer_detail)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
