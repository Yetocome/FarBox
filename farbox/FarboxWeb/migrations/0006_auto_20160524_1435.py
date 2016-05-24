# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FarboxWeb', '0005_auto_20160524_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realfile',
            name='file_hash',
            field=models.CharField(max_length=200),
        ),
    ]
