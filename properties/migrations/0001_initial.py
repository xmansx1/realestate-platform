# Generated by Django 5.1.7 on 2025-03-24 05:44

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(blank=True, verbose_name='نبذة عنا')),
                ('whatsapp', models.CharField(blank=True, max_length=20, verbose_name='رقم الواتساب')),
                ('twitter', models.URLField(blank=True, verbose_name='رابط تويتر')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='رقم الهاتف')),
                ('snapchat', models.URLField(blank=True, verbose_name='رابط سناب شات')),
            ],
            options={
                'verbose_name': 'إعدادات الفوتر',
                'verbose_name_plural': 'إعدادات الفوتر',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان الخبر')),
                ('is_active', models.BooleanField(default=True, verbose_name='مفعل؟')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('request_type', models.CharField(choices=[('sell', 'بيع'), ('rent', 'إيجار')], max_length=10)),
                ('owner_type', models.CharField(choices=[('owner', 'مالك مباشر'), ('agent', 'وسيط عقاري')], max_length=10)),
                ('property_type', models.CharField(choices=[('apartment', 'شقة'), ('villa', 'فيلا'), ('floor', 'دور'), ('land', 'أرض'), ('building', 'عمارة')], max_length=20)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('area', models.FloatField()),
                ('details', models.TextField(blank=True)),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='وصف العقار')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('is_finance_available', models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='properties.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('buy', 'شراء'), ('rent', 'استئجار'), ('sell', 'بيع')], max_length=10)),
                ('owner_type', models.CharField(choices=[('owner', 'مالك'), ('broker', 'وسيط')], max_length=10)),
                ('property_type', models.CharField(choices=[('apartment', 'شقة'), ('villa', 'فيلا'), ('building', 'عمارة'), ('land', 'أرض')], max_length=20)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('area', models.DecimalField(decimal_places=2, max_digits=10)),
                ('full_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('details', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
