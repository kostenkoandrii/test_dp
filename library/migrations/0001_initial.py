# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('author', models.ForeignKey(to='library.Author', related_name='books')),
            ],
        ),
        migrations.CreateModel(
            name='BookLoanJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('planned_return_date', models.DateField()),
                ('actual_return_date', models.DateField(null=True, blank=True)),
                ('book', models.ForeignKey(to='library.Book', related_name='loan_records')),
            ],
        ),
        migrations.CreateModel(
            name='BookSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('page_number', models.IntegerField()),
                ('article_name', models.CharField(max_length=255)),
                ('book', models.ForeignKey(to='library.Book', related_name='summary')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=13)),
                ('address', models.CharField(max_length=225)),
            ],
        ),
        migrations.AddField(
            model_name='bookloanjournal',
            name='client',
            field=models.ForeignKey(to='library.Client', related_name='loan_records'),
        ),
        migrations.AlterUniqueTogether(
            name='booksummary',
            unique_together=set([('article_name', 'book')]),
        ),
        migrations.AlterUniqueTogether(
            name='book',
            unique_together=set([('name', 'author')]),
        ),
    ]
