# Generated by Django 2.0.8 on 2019-02-10 08:20

import apps.read_statistics.Mixin
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_updated_time', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
            ],
            options={
                'verbose_name': '博客',
                'verbose_name_plural': '博客',
                'ordering': ['-create_time'],
            },
            bases=(models.Model, apps.read_statistics.Mixin.ReadTimeExpandMixin),
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=10, verbose_name='博客分类')),
            ],
            options={
                'verbose_name': '博客分类',
                'verbose_name_plural': '博客分类',
            },
        ),
    ]
