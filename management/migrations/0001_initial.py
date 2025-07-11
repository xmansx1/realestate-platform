# Generated by Django 5.2.4 on 2025-07-07 01:33

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
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='اسم العقار')),
                ('city', models.CharField(max_length=100, verbose_name='المدينة')),
                ('district', models.CharField(max_length=100, verbose_name='الحي')),
                ('is_approved', models.BooleanField(default=False, verbose_name='تمت الموافقة')),
                ('deed_document', models.FileField(blank=True, null=True, upload_to='documents/deeds/', verbose_name='صك الملكية')),
                ('insurance_document', models.FileField(blank=True, null=True, upload_to='documents/insurance/', verbose_name='وثيقة التأمين')),
                ('sketch_document', models.FileField(blank=True, null=True, upload_to='documents/sketches/', verbose_name='الكروكي')),
                ('agency_document', models.FileField(blank=True, null=True, upload_to='documents/agency/', verbose_name='وكالة شرعية')),
                ('other_document', models.FileField(blank=True, null=True, upload_to='documents/other/', verbose_name='مستند آخر')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_properties', to=settings.AUTH_USER_MODEL, verbose_name='المالك')),
            ],
            options={
                'verbose_name': 'عقار',
                'verbose_name_plural': 'العقارات',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_number', models.CharField(max_length=50, verbose_name='رقم الوحدة')),
                ('area', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='المساحة (م²)')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='السعر')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='الموقع (اختياري)')),
                ('status', models.CharField(choices=[('available', 'متاح'), ('sold', 'مباع'), ('rented', 'مؤجر'), ('maintenance', 'صيانة')], default='available', max_length=20, verbose_name='حالة الوحدة')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='ملاحظات')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإضافة')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_units', to=settings.AUTH_USER_MODEL, verbose_name='الموظف المسؤول')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='management.property', verbose_name='العقار')),
            ],
            options={
                'verbose_name': 'وحدة',
                'verbose_name_plural': 'الوحدات',
            },
        ),
        migrations.CreateModel(
            name='ScheduledMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_type', models.CharField(max_length=100, verbose_name='نوع الصيانة')),
                ('scheduled_date', models.DateField(verbose_name='تاريخ الصيانة المجدولة')),
                ('description', models.TextField(blank=True, null=True, verbose_name='الوصف')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_maintenances', to='management.unit', verbose_name='الوحدة')),
            ],
            options={
                'verbose_name': 'صيانة مجدولة',
                'verbose_name_plural': 'الصيانات المجدولة',
            },
        ),
        migrations.CreateModel(
            name='RentalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='تاريخ البداية')),
                ('end_date', models.DateField(verbose_name='تاريخ النهاية')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='قيمة الإيجار')),
                ('tenant_name', models.CharField(max_length=255, verbose_name='اسم المستأجر')),
                ('unit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rental_info', to='management.unit', verbose_name='الوحدة')),
            ],
            options={
                'verbose_name': 'عقد إيجار',
                'verbose_name_plural': 'عقود الإيجار',
            },
        ),
        migrations.CreateModel(
            name='UpdateLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_type', models.CharField(max_length=100, verbose_name='نوع التحديث')),
                ('date', models.DateField(verbose_name='تاريخ التحديث')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='المبلغ')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='unit_updates/', verbose_name='مرفق')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='management.unit', verbose_name='الوحدة')),
            ],
            options={
                'verbose_name': 'تحديث/مصروف',
                'verbose_name_plural': 'التحديثات والمصروفات',
            },
        ),
    ]
