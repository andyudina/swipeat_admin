# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import editorial.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441')),
                ('order_number', models.IntegerField(default=editorial.models.next_question_number, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x80\xd1\x8f\xd0\xb4\xd0\xba\xd0\xbe\xd0\xb2\xd1\x8b\xd0\xb9 \xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80')),
            ],
            options={
                'verbose_name': '\u0412\u043e\u043f\u0440\u043e\u0441',
                'verbose_name_plural': '\u0412\u043e\u043f\u0440\u043e\u0441\u044b',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mongo_id', models.CharField(max_length=255, verbose_name='ID MONGO')),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('is_compeleted', models.BooleanField(default=False, verbose_name='\u0417\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u043e')),
                ('feautures_vector', models.IntegerField(default=False, verbose_name='\u0411\u0438\u0442\u043e\u0432\u044b\u0439 \u0432\u0435\u043a\u0442\u043e\u0440 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a')),
                ('allowed_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438, \u0443 \u043a\u043e\u0442\u043e\u0440\u044b\u0445 \u0435\u0441\u0442\u044c \u0434\u043e\u0441\u0442\u0443\u043f', blank=True)),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0441\u0442\u043e\u0440\u0430\u043d',
                'verbose_name_plural': '\u0420\u0435\u0441\u0442\u043e\u0440\u0430\u043d\u044b',
            },
        ),
        migrations.CreateModel(
            name='RestoToQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_true', models.BooleanField(default=False)),
                ('question', models.ForeignKey(to='editorial.Question')),
                ('restaurant', models.ForeignKey(to='editorial.Restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='question_answers',
            field=models.ManyToManyField(to='editorial.Question', verbose_name='\u041e\u0442\u0432\u0435\u0442\u044b \u043d\u0430 \u0432\u043e\u043f\u0440\u043e\u0441\u044b', through='editorial.RestoToQuestion', blank=True),
        ),
    ]
