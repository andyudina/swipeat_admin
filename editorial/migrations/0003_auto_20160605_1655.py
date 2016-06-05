# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0002_auto_20160605_0929'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='feautures_vector',
            new_name='features_vector',
        ),
    ]
