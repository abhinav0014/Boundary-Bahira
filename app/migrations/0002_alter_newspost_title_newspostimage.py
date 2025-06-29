# Generated by Django 5.2.3 on 2025-06-20 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newspost",
            name="title",
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name="NewsPostImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="news_images/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "news_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="app.newspost",
                    ),
                ),
            ],
        ),
    ]
