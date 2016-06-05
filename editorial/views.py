# -*- coding: utf-8 -*-
#import json

from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotFound, JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic.base import View, TemplateView
from django.core.mail import send_mail

from .models import Restaurant, Question, RestoToQuestion
from .decorators import can_see_restaurant 
from .utils import to_boolean, generate_password
from swipeeat import settings

class BaseView(View):
    _BaseView__ERRORS = {
        'not_enough_answers': u'Ответьте на все вопросы',  
        'invalid_credentials': u'Неверный логин и/или пароль' 
    }
    
        
    def error(self, request, code, context={}):
        error_ = {
            'message': self.__ERRORS.get(code),
            'code': code,
        }
        context.update({'error': error_})
        return render(request, self.template_name, context)
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
        
class RestaurantListView(View):
    template_name = 'editorial/list.html'
    
    def get(self, request, *args, **kwargs):
        #if request.GET.get('all'):
        new_restaurants = Restaurant.objects.get_new_alloweded(user=request.user)
        #elif request.GET.get('done'):
        completed_restaurants = Restaurant.objects.get_done_alloweded(user=request.user) 
        #else:
        all_restaurants = Restaurant.objects.get_all_alloweded(user=request.user)
        return render(request, self.template_name, {
            'new_restaurants': new_restaurants,
            'completed_restaurants': completed_restaurants,
            'all_restaurants': all_restaurants,
        })

                   
class RestaurantOneView(BaseView):
    template_name = 'editorial/one.html'
    
    @can_see_restaurant
    def get(self, request, restaurant, *args, **kwargs):
        return render(request, self.template_name, {
            'restaurant': restaurant.to_json(),
        })    
 
    #expected format: <question_id1>=<answer1>&<question_id2>=<answer2>...
    @can_see_restaurant
    def post(self, request, restaurant, *args, **kwargs):
        questions = Question.objects.order_by('order_number')
        answers = request.POST
        for question in questions:
            try: 
                is_true = to_boolean(answers.get(str(question.id)))
            except ValueError:
                return HttpResponseBadRequest(self.error(request, 'not_enough_answers', {
                'restaurant': restaurant.to_json(),
            }))
            restaurant.answer_to_question(question=question, is_true=is_true)
        restaurant.complete()
        return HttpResponseRedirect('/')        
        
        
class LoginView(BaseView):
    template_name = 'editorial/login.html'
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist, MutipleObejctsReturned:
            return HttpResponseForbidden(self.error(request, 'invalid_credentials'))
        user = authenticate(username=user.username, password=password)
        if not user:
            return HttpResponseForbidden(self.error(request, 'invalid_credentials'))
        login(request, user)
        return HttpResponseRedirect(request.GET.get('next', '/'))
       
class SendPasswordView(View):
    template_name = 'editorial/send_password_success.html'
    
    def _send_password_email(self, **kwargs):
        send_mail(
            '[SwipeEat] Ваш новый пароль на SwipeEat ',
            'Пароль: {}'. format(kwargs.get('password')),
            settings.EMAIL_HOST_USER,
            [kwargs.get('email'), ]
        )
        
    def _set_new_password(self, user):
        new_password = generate_password()
        user.set_password(new_password)
        user.save()
        self._send_password_email(email=user.email, password=new_password)
        
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('user_id'))
        except User.DoesNotExist:
            return HttpResponseNotFound()
        self._set_new_password(user)   
        return render(request, self.template_name)
            
class AssignRestaurantsView(View):
    template_name = 'editorial/assign_success.html'

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('user_id'))
        except User.DoesNotExist:
            return HttpResponseNotFound()
        restaurants = Restaurant.objects.filter(allowed_users=None)
        for restaurant in restaurants:
            restaurant.allowed_users.add(user)
        return render(request, self.template_name, {
            'resto_count': len(restaurants),
            'user': user.email
        })       
