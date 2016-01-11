# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from src.aggregates.agreement_type.services import agreement_type_service
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):
  dependencies = [
    ('user', '0001_initial'),
  ]

  def create_defaults(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    agreement_type_service.create_agreement_type('Consulting', True, None)
    agreement_type_service.create_agreement_type('Licensing', True, None)
    agreement_type_service.create_agreement_type('Sales', True, None)

  operations = [
    migrations.CreateModel(
      name='AgreementType',
      fields=[
        ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
        ('agreement_type_id', models.CharField(unique=True, max_length=8)),
        ('agreement_type_name', models.CharField(max_length=2400)),
        ('agreement_type_global', models.BooleanField()),
        ('agreement_type_system_created_date', models.DateTimeField()),
        ('agreement_type_user',
         models.ForeignKey(null=True, to='user.User', blank=True, to_field='user_id', related_name='agreement_types')),
      ],
      bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
    ),
    migrations.AlterUniqueTogether(
      name='agreementtype',
      unique_together=set([('agreement_type_name', 'agreement_type_user')]),
    ),
    migrations.RunPython(create_defaults),
  ]
