# Generated by Django 3.2.9 on 2023-07-22 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_auto_20230722_1717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todoitem',
            old_name='category',
            new_name='category',
        ),
    ]