# Generated by Django 4.2 on 2023-04-07 18:20

import app.accounts.models
from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_alter_userprofile_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_image",
            field=imagekit.models.fields.ProcessedImageField(
                default="default.jpg",
                upload_to=app.accounts.models.get_profile_image_filename,
            ),
        ),
    ]
