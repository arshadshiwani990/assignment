# Generated by Django 5.1.3 on 2024-11-21 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_student_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.IntegerField(max_length=15),
        ),
    ]