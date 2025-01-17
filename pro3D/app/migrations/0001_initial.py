# Generated by Django 3.2.5 on 2023-04-07 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_account', models.CharField(default='zhangsan', max_length=50)),
                ('user_password', models.CharField(default='123456', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('project_name', models.CharField(max_length=100)),
                ('build_time', models.TimeField(auto_now_add=True)),
                ('remark', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='CTSet',
            fields=[
                ('set_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('set_name', models.CharField(max_length=100)),
                ('directory', models.CharField(max_length=200)),
                ('original_path', models.CharField(max_length=200)),
                ('nii_path', models.CharField(max_length=200)),
                ('label_path', models.CharField(max_length=200)),
                ('nii_after_path', models.CharField(max_length=200)),
                ('stl_directory', models.CharField(max_length=200)),
                ('build_time', models.TimeField(auto_now_add=True)),
                ('remark', models.TextField()),
                ('projects', models.ManyToManyField(to='app.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.IntegerField()),
                ('organ_name', models.CharField(max_length=100)),
                ('r', models.IntegerField()),
                ('g', models.IntegerField()),
                ('b', models.IntegerField()),
                ('transparency', models.FloatField()),
                ('visible', models.BooleanField()),
                ('stl_path', models.CharField(max_length=200)),
                ('ct_set', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.ctset')),
            ],
            options={
                'unique_together': {('ct_set', 'label')},
            },
        ),
    ]
