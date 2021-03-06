# -*- coding: utf-8 -*-
from django.db import models, connection

def next_question_number():
    return (Question.objects.count() or 0) + 1
    
class Question(models.Model):
    question = models.TextField(u'Вопрос')
    order_number = models.IntegerField('Порядковый номер', default=next_question_number)

    def __unicode__(self):
         return self.question
         
    class Meta:
        verbose_name = u"Вопрос"
        verbose_name_plural = u"Вопросы" 


class RestaurantManager(models.Manager):
    def _form_base_filter(self, user):
        if user is None:
            raise ValueError('No user')
        if user.is_staff:
            return {}
        return {'allowed_users__id__in': [user.id, ]}
        
    def get_all_alloweded(self, **kwargs):
        filters = self._form_base_filter(kwargs.get('user'))
        return self.filter(**filters)
        
    def get_done_alloweded(self, **kwargs): 
        filters = self._form_base_filter(kwargs.get('user'))
        filters['is_completed'] = True
        return self.filter(**filters)
        
    def get_new_alloweded(self, **kwargs):
        filters = self._form_base_filter(kwargs.get('user'))
        filters['is_completed'] = False
        return self.filter(**filters)
                      
class Restaurant(models.Model):
    mongo_id = models.CharField(u'ID MONGO', max_length=255)
    title = models.CharField(u'Название', max_length=255)
    is_completed = models.BooleanField(u'Заполнено', default=False)
    features_vector = models.IntegerField(u'Битовый вектор характеристик', default =0)
    allowed_users = models.ManyToManyField('auth.User', verbose_name=u'Пользователи, у которых есть доступ', blank=True)
    question_answers = models.ManyToManyField('Question', verbose_name=u'Ответы на вопросы', blank=True, through='RestoToQuestion')
    
    objects = RestaurantManager()
    
    def __unicode__(self):
         return self.title
      
    def answer_to_question(self, **kwargs):
        obj, created = RestoToQuestion.objects.get_or_create(
            question=kwargs.get('question'), 
            restaurant=self
        )
        obj.is_true = kwargs.get('is_true')
        obj.save()
        
    def complete(self):
        self.is_completed = True
        self._generate_features_vector()
        self.save(update_fields=['is_completed', 'features_vector']) 
        
    def _generate_features_vector(self):
        self.features_vector = 0
        for question in RestoToQuestion.objects.filter(restaurant__id=self.id).order_by('question__order_number'):
            self.features_vector <<= 1
            self.features_vector += int(question.is_true)
            print self.features_vector, int(question.is_true)
      
    def to_json_short(self):
        return {
            'id': self.id,
            'title': self.title,
            'is_completed': self.is_completed
        }
        
    def to_json(self):
        json_ = self.to_json_short()
        json_['questions'] = RestoToQuestion.objects.get4resto_json(self)
        return json_
       
    @property
    def allowed_user_ids(self):
        return [x.id for x in self.allowed_users.all()]
        
    class Meta:
        verbose_name = u"Ресторан"
        verbose_name_plural = u"Рестораны" 
        
        
class RestoToQuestionManager(models.Manager):
    def get4resto_json(self, resto):
        cursor = connection.cursor()
        APP_NAME = 'editorial'
        cursor.execute('''
            SELECT q.id, q.question, q.order_number, COALESCE(r.is_true, 0)
            FROM {}_question q LEFT JOIN {}_restotoquestion r on q.id = r.question_id AND r.restaurant_id=%s
            ORDER BY q.order_number
        '''.format(*([APP_NAME, ] * 2)), [resto.id])
        COLUMNS = ['id', 'question', 'order_number', 'is_true']
        return [
            dict(zip(COLUMNS, row))
            for row in cursor.fetchall()
        ]
        
class RestoToQuestion(models.Model):
    question = models.ForeignKey('Question')
    restaurant = models.ForeignKey('Restaurant')
    is_true = models.BooleanField(default=False)
    objects = RestoToQuestionManager()
    
    unique_together = (("question", "restaurant"),)
    
    def __unicode__(self):
         return u'Вопрос №{}'.format(self.question.order_number)
        
   

        
    
