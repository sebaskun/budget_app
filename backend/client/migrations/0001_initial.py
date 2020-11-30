# Generated by Django 2.0.6 on 2018-09-25 06:34

import backend.core.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', backend.core.utils.CharNullField(max_length=150, verbose_name='nombre')),
                ('short_name', backend.core.utils.CharNullField(blank=True, max_length=40, null=True, verbose_name='nombre corto')),
                ('initials', backend.core.utils.CharNullField(max_length=3, verbose_name='iniciales')),
                ('ruc', backend.core.utils.CharNullField(blank=True, max_length=11, null=True, verbose_name='RUC')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='dirección')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='client', verbose_name='logo')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'permissions': (('can_add_client', 'Puede adicionar cliente'), ('can_edit_client', 'Puede modificar cliente'), ('can_change_status_client', 'Puede cambiar estado cliente'), ('can_see_view_client', 'Puede ver cliente')),
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=128, verbose_name='nombre')),
                ('cargo', models.CharField(blank=True, max_length=35, null=True, verbose_name='cargo')),
                ('observacion', models.CharField(blank=True, max_length=100, null=True, verbose_name='observación')),
                ('position', models.PositiveIntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients_contact', to='client.Client', verbose_name='cliente')),
            ],
            options={
                'verbose_name': 'contacto',
                'verbose_name_plural': 'contactos',
            },
        ),
        migrations.CreateModel(
            name='MeansContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(0, 'Teléfono'), (1, 'Celular'), (2, 'Correo'), (3, 'Otros')], default=0, verbose_name='tipo')),
                ('dato', models.CharField(max_length=35, verbose_name='dato')),
                ('observacion', models.CharField(blank=True, max_length=100, null=True, verbose_name='observación')),
                ('position', models.PositiveIntegerField()),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.Contact')),
            ],
            options={
                'verbose_name': 'medio de contacto',
                'verbose_name_plural': 'medios de contacto',
            },
        ),
    ]