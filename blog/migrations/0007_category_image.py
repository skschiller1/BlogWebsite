# Generated by Django 4.1.7 on 2023-07-12 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_options_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=1, upload_to='C:\\Users\\Samuel\\PycharmProjects\\ActualBlogWebsite\\myblogsite\\media'),
            preserve_default=False,
        ),
    ]
