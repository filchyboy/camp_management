# Generated by Django 4.2 on 2023-04-06 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_interview_interviewmention"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="assigned_interviewee",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assigned_interviewee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="assigned_interviewer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assigned_interviewer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]