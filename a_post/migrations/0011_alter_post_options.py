# Generated by Django 5.1.1 on 2024-10-29 14:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("a_post", "0010_post_author"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-modified_at"]},
        ),
    ]
