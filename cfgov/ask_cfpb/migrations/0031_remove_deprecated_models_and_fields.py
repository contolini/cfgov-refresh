# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-18 00:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0030_remove_answer_category_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='related_subcategories',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer_es',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='audiences',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='category',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='featured',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='featured_rank',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='last_edited',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='last_edited_es',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='next_step',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='question_es',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='related_questions',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='search_tags',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='search_tags_es',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='slug_es',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='snippet',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='snippet_es',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='social_sharing_image',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='statement',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='subcategory',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='update_english_page',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='update_spanish_page',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='answerpage',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='answerpage',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='Audience',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
