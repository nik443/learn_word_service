# Generated by Django 4.1.7 on 2023-09-22 01:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base_site', '0014_alter_userdictionaries_dictionary_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDictionariesNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_training_date', models.DateTimeField(verbose_name='последняя тренировка')),
                ('last_training_result', models.BooleanField(verbose_name='результат последней тренировки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_site.masterdictionaries')),
            ],
        ),
    ]