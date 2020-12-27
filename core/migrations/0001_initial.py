# Generated by Django 3.1.4 on 2020-12-27 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nursury', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(blank=True, decimal_places=3, default=1, max_digits=19, null=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nursury.plant')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('ordered', models.BooleanField(default=False)),
                ('ordered_on', models.DateTimeField(blank=True, null=True)),
                ('details', models.ManyToManyField(related_name='order_details', to='core.OrderDetails')),
                ('placed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_placed_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]