# Generated by Django 3.2.9 on 2021-11-15 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_auto_20211111_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='guideline',
            name='funcName',
            field=models.TextField(db_column='funName', default=''),
        ),
        migrations.AddField(
            model_name='guideline',
            name='orderName',
            field=models.TextField(db_column='orderName', default=''),
        ),
        migrations.AlterField(
            model_name='qna',
            name='answer',
            field=models.TextField(db_column='answer', null=True),
        ),
    ]
