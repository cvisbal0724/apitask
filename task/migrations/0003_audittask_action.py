# Generated by Django 5.2.4 on 2025-07-19 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_audittask_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='audittask',
            name='action',
            field=models.CharField(choices=[('creado', 'Creado'), ('actualizado', 'Actualizado'), ('eliminado', 'Eliminado')], default='creado', max_length=255),
        ),
    ]
