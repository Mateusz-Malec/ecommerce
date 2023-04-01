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
                  # path('products/<c_id>', views.computer_detail)
                  # path('computers/<c_id>', views.AboutView.as_view())
                  path('cart/', views.cart_view, name='cart'),
                  path('cart/add/<p_id>', views.add_to_cart, name='add_to_cart'),
                  path('signup/', views.signup_page, name='signup'),
                  path('login/', views.login_page, name='login'),
                  path('logout/', views.logout_page, name='logout'),
                  path('userprofile/',views.user_profile,name='userprofile')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
