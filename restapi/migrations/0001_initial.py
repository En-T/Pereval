# Generated by Django 3.2.13 on 2022-06-09 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longtude', models.FloatField()),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.ImageField(upload_to='uploads')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Pereval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('other_titles', models.CharField(max_length=64)),
                ('status', models.CharField(choices=[('n', 'Новый'), ('p', 'В ожидании'), ('a', 'Принято'), ('r', 'Отклонено')], default='n', max_length=1)),
                ('connect', models.TextField()),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('l_winter', models.CharField(max_length=10)),
                ('l_summer', models.CharField(max_length=10)),
                ('l_autumn', models.CharField(max_length=10)),
                ('l_spring', models.CharField(max_length=10)),
                ('coords', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.coords')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Pereval_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.images')),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.pereval')),
            ],
        ),
        migrations.AddField(
            model_name='pereval',
            name='images',
            field=models.ManyToManyField(through='restapi.Pereval_Images', to='restapi.Images'),
        ),
        migrations.AddField(
            model_name='pereval',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.user'),
        ),
    ]
