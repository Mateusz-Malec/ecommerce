from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views
from .views import ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('desktops/', views.computers_, name='desktops'),
                  path('laptops/', views.laptops, name='laptops'),
                  path('products/<c_id>/', views.details, name='products'),
                  # path('products/<c_id>', views.computer_detail)
                  # path('computers/<c_id>', views.AboutView.as_view())
                  path('cart/', views.cart_view, name='cart'),
                  path('cart/add/<p_id>/', views.add_to_cart, name='add_to_cart'),
                  path('cart/update/<p_id>/<quant>', views.update_product_in_cart, name='update_product_in_cart'),
                  path('cart/remove/<p_id>/', views.remove_from_cart, name='remove_from_cart'),
                  path('generate/', views.generatePDF, name='order_generate'),
                  path('signup/', views.signup_page, name='signup'),
                  path('login/', views.login_page, name='login'),
                  path('logout/', views.logout_page, name='logout'),
                  path('userprofile/', views.user_profile, name='userprofile'),
                  path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
                  path('password-reset-confirm/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
                       name='password_reset_confirm'),
                  path('password-reset-complete/',
                       auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
                       name='password_reset_complete')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
