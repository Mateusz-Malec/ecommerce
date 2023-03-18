from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('desktops/', views.computers_, name='desktops'),
                  path('laptops/', views.laptops, name='laptops'),
                  path('products/<c_id>/', views.details, name='products'),
                  #path('products/<c_id>', views.computer_detail)
                  # path('computers/<c_id>', views.AboutView.as_view())
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
