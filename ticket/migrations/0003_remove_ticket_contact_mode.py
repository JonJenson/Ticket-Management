# Generated by Django 4.2.7 on 2023-11-25 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_alter_ticket_engineer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='contact_mode',
        ),
    ]