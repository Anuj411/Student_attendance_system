# Generated by Django 3.2.9 on 2022-09-10 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_alter_attendance_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
