# Generated by Django 5.2.4 on 2025-07-06 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(max_length=100, verbose_name='المدينة'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الانضمام'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='district',
            field=models.CharField(max_length=100, verbose_name='الحي'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='البريد الإلكتروني'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(max_length=150, verbose_name='الاسم الكامل'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='نشط'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='موظف إداري'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=15, unique=True, verbose_name='رقم الجوال'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'مدير'), ('agent', 'وسيط'), ('owner', 'مالك'), ('manager', 'موظف إداري')], max_length=20, verbose_name='الدور'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='val_license',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='رقم الرخصة'),
        ),
    ]
