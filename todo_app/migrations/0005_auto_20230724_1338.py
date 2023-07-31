# Generated by Django 3.2.9 on 2023-07-24 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0004_todoitem_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todoitem',
            old_name='category',
            new_name='department',
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='status',
            field=models.CharField(choices=[('w', 'Writing'), ('e', 'Editing'), ('l', 'Linkedin'), ('j', 'Journal'), ('i', 'Linkedin & Journal')], max_length=1),
        ),
    ]