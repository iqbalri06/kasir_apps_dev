from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from . import views

app_name = 'simple_shop'

urlpatterns = [
    # Root URL redirects to login if not authenticated
    path('', lambda request: redirect('simple_shop:login') if not request.user.is_authenticated else redirect('simple_shop:dashboard'), name='root'),
    path('accounts/login/', lambda request: redirect('simple_shop:login'), name='auth_login'),
    
    # Login/Logout URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard URL (only accessible after login)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin URLs
    path('products/', views.product_list, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<uuid:product_id>/', views.product_detail, name='product_detail'),
    path('products/<uuid:product_id>/delete/', views.delete_product, name='delete_product'),
    
    # Sales URLs - fixed the duplicate path by using a single path with both names
    path('sales/', views.sale_list, name='sales'),  # Primary sales list URL
    path('sales/new/', views.new_sale, name='new_sale'),
    path('sales/<uuid:sale_id>/', views.sale_detail, name='sale_detail'),
    path('sales/checkout/', views.checkout, name='checkout'),
    path('sales/<uuid:sale_id>/print/', views.print_receipt, name='print_receipt'),
    
    # Member URLs - Make sure the print URL is correct
    path('members/card/<uuid:member_id>/print/', views.print_member_card, name='print_member_card'),
    # Remove the invalid path that was causing the error
    path('members/search/api/', views.member_search_api, name='member_search_api'),
    path('members/register/api/', views.member_register_api, name='member_register_api'),
    path('members/register/', views.register_member, name='register_member'),
    path('members/search/', views.search_member, name='search_member'),
    path('members/', views.member_search_page, name='member_search_page'),

    # User URLs
    path('users/', views.user_list, name='users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/<uuid:pk>/', views.user_detail, name='user_detail'),
    path('users/<uuid:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<uuid:uuid>/update/', views.user_update, name='user_update'),
    path('users/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('profile/', views.profile, name='profile'),  # New URL for profile

    # Cashier URLs
    path('cashier/', views.cashier, name='cashier'),

    # Cart URLs
    path('cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<uuid:item_id>/', views.remove_from_cart_ajax, name='remove_from_cart_ajax'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    # Export URLs
    path('export/sales/', views.export_sales, name='export_sales'),

    # Password reset URLs
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('debug/sales/', views.debug_sales, name='debug_sales'),
    ]
