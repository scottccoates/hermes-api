# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('agreement_type', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialAgreement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('uid', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(max_length=2400)),
                ('artifacts', jsonfield.fields.JSONField(default=list)),
                ('counterparty', models.CharField(blank=True, null=True, max_length=2400)),
                ('description', models.TextField(blank=True, null=True)),
                ('execution_date', models.DateTimeField(blank=True, null=True)),
                ('term_length_time_amount', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('term_length_time_type', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('auto_renew', models.NullBooleanField()),
                ('outcome_notice_time_amount', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('outcome_notice_time_type', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('outcome_notice_alert_enabled', models.NullBooleanField()),
                ('outcome_notice_alert_time_amount', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('outcome_notice_alert_time_type', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('expiration_alert_enabled', models.NullBooleanField()),
                ('expiration_alert_time_amount', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('expiration_alert_time_type', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('duration_details', models.TextField(blank=True, null=True)),
                ('completed', models.BooleanField()),
                ('system_created_date', models.DateTimeField()),
                ('agreement_type', models.ForeignKey(blank=True, null=True, to_field='uid', to='agreement_type.AgreementType', related_name='potential_agreements')),
                ('user', models.ForeignKey(related_name='potential_agreements', to='user.User', to_field='uid')),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
