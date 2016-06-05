from .models import Restaurant
from django.http import HttpResponseForbidden, HttpResponseNotFound

def can_see_restaurant(view_method):
    def wrapper(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(id=kwargs.get('restaurant_id'))
        except Restaurant.DoesNotExist:
            return HttpResponseNotFound()
            
        if request.user.is_authenticated() and (request.user.is_staff or request.user.id in restaurant.allowed_user_ids):
            return view_method(self, request, restaurant, *args, **kwargs)
        return HttpResponseForbidden()
    return wrapper
    
def login_required(view_method):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_active:
            return view_method(self, request, *args, **kwargs)
        return HttpResponseForbidden()
    return wrapper 
