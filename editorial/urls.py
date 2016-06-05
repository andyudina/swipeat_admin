# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from editorial.views import RestaurantListView, RestaurantOneView, LoginView, SendPasswordView, AssignRestaurantsView

login_redirect_decorator = login_required(login_url='/login/')

urlpatterns = [
    url(r'^$', 
        login_redirect_decorator(RestaurantListView.as_view())),
    url(r'^login/$', 
        LoginView.as_view()),
    url(r'^(?P<restaurant_id>\d+)/$', 
        login_redirect_decorator(csrf_exempt(RestaurantOneView.as_view()))),
    url(r'^userpassword/(?P<user_id>\d+)/$', 
        staff_member_required(csrf_exempt(SendPasswordView.as_view()))),
    url(r'^assignresttouser/(?P<user_id>\d+)/$', 
        staff_member_required(AssignRestaurantsView.as_view())),  
]
