# Generated by Django 5.1.1 on 2024-09-24 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('score', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessment_type', models.CharField(choices=[('Cognitive Status', 'Cognitive Status'), ('Physical Health', 'Physical Health'), ('Mental Health', 'Mental Health'), ('Functional Ability', 'Functional Ability'), ('Social Support', 'Social Support')], default='Cognitive Status', max_length=50)),
                ('assessment_date', models.DateField()),
                ('final_score', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('assessment_type', models.CharField(max_length=50)),
            ],
        ),
    ]
