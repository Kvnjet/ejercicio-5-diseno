from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Fiesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('ubicacion', models.CharField(max_length=300)),
                ('latitud', models.FloatField(blank=True, null=True)),
                ('longitud', models.FloatField(blank=True, null=True)),
                ('capacidad', models.PositiveIntegerField()),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('descripcion', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'fiestas', 'ordering': ['fecha', 'hora']},
        ),
        migrations.CreateModel(
            name='Invitado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('contacto', models.CharField(max_length=200)),
                ('estado', models.CharField(
                    choices=[('pendiente', 'Pendiente'), ('confirmado', 'Confirmado'), ('rechazado', 'Rechazado')],
                    default='pendiente', max_length=20,
                )),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('fiesta', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='invitados',
                    to='backend.fiesta',
                )),
            ],
            options={'db_table': 'invitados', 'ordering': ['registered_at']},
        ),
    ]
