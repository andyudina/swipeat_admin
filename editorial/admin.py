# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter

from .models import Question, Restaurant, RestoToQuestion

admin.site.register(Question)

class QuestionInline(admin.TabularInline):
    model = Restaurant.question_answers.through
    verbose_name = u"Вопрос"
    verbose_name_plural = u"Вопросы"

class EmployeeFilter(SimpleListFilter):
    title = u'Кто заполняет'
    parameter_name = 'allowed_users'

    def lookups(self, request, model_admin):
        return [(u.id, u.email) for u in User.objects.filter(is_staff=False)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(allowed_users__id__in=[self.value()])
        else:
            return queryset
            
class RestaurantAdmin(admin.ModelAdmin):
    list_filter = ('is_completed', EmployeeFilter)
    exclude = ("question_answers", )
    inlines = (
       QuestionInline,
    )
    extra = 0
        
admin.site.register(Restaurant, RestaurantAdmin)

admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'button_send_password', 'button_assign_restaurants')
                
    def button_send_password(self, instance):
        return mark_safe(u'<a href="/userpassword/' + str(instance.id) + u'/">Отправить пароль</a>')
                
    def button_assign_restaurants(self, instance):
        return mark_safe(u'<a href="/assignresttouser/' + str(instance.id) + u'/">Назначить неназначенные рестораны</a>')
        
admin.site.register(User, CustomUserAdmin)
