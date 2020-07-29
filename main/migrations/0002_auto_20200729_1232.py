# Generated by Django 3.0.7 on 2020-07-29 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('pub_date', models.DateField(blank=True)),
                ('affiche', models.ImageField(upload_to='affiches')),
                ('description', models.TextField(blank=True)),
                ('facebook_link', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
