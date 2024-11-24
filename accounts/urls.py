# from django.urls import path
# from . import views


# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('', views.landing_page_view, name='home'),  

    
# ]

from django.urls import path
from .views import login_view, register_view, landing_page_view
from . import views
urlpatterns = [
    path('', landing_page_view, name='landing'),  # Landing page URL
    path('login/', login_view, name='login'),      # Login page URL
    path('register/', register_view, name='register'),  # Registration page URL
    path('logout/', login_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'), 
    path('change-password/', views.change_password, name='change_password'),   
]


