# Generated by Django 5.2.4 on 2025-07-08 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0008_delete_deal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestaterequest',
            name='status',
            field=models.CharField(choices=[('new', 'جديد'), ('reviewed', 'تم المراجعة'), ('contacted', 'تم التواصل'), ('executed', 'تم التنفيذ')], default='new', max_length=20),
        ),
    ]
