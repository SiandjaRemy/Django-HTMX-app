# Generated by Django 5.1.1 on 2024-11-13 08:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a_post", "0018_likedreply_commentreply_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(related_name="posts", to="a_post.tag"),
        ),
    ]
