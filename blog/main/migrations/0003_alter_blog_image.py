# Generated by Django 5.0.7 on 2024-07-31 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_blog_id_remove_comment_id_alter_blog_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog/image'),
        ),
    ]
