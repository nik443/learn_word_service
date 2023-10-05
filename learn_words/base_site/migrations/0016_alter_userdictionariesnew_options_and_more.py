# Generated by Django 4.1.7 on 2023-10-04 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base_site', '0015_userdictionariesnew'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdictionariesnew',
            options={'ordering': ['last_training_result', '-last_training_date']},
        ),
        migrations.AlterField(
            model_name='userdictionariesnew',
            name='last_training_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='последняя тренировка'),
        ),
        migrations.AlterField(
            model_name='userdictionariesnew',
            name='last_training_result',
            field=models.BooleanField(default=False, verbose_name='результат последней тренировки'),
        ),
        migrations.CreateModel(
            name='DatesLastAddedWordInUserDict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_last_added_word', models.DateTimeField(default=django.utils.timezone.now, verbose_name='последнее слово добавлено')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
