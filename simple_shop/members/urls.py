from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.member_search_page, name='member_search_page'),
    path('search/api/', views.member_search_api, name='member_search_api'),
    path('register/api/', views.member_register_api, name='member_register_api'),
    path('card-template/', views.member_card_template, name='member_card_template'),
    path('debug/search/', views.debug_search_page, name='debug_search_page'),   # Add this debug route
    path('debug/', views.debug_view, name='debug'),
    path('test-api/', views.test_api_page, name='test_api'),
    path('debug/form/', views.debug_form, name='debug_form'),
    path('download-card/<uuid:member_id>/', views.download_member_card, name='download_card'),
]