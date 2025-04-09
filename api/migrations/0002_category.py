# Generated by Django 5.1.7 on 2025-04-02 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('products', models.ManyToManyField(related_name='categories', to='api.product')),
            ],
        ),
    ]
