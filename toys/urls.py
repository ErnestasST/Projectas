from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_drawing, name='upload_drawing'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('toys/', views.toy_list, name='toy_list'),
    path('toys/<int:id>/', views.toy_details, name='toy_details'),
    path('add_toy/', views.add_toy, name='add_toy'),
    path('add_accessory/', views.add_accessory, name='add_accessory'),
    path('update_cart/<int:item_id>/<int:action>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('track_drawings/', views.track_drawings, name='track_drawings'),
    path('edit_drawing/<int:id>/', views.edit_drawing, name='edit_drawing'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)