import django.core.validators
import django_better_admin_arrayfield.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workplace', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=30)),
                ('period', models.CharField(max_length=50)),
                ('image', models.ImageField(help_text='Rasio harus persegi. Contoh: 600px \xd7 600px', upload_to='experience/')),
                ('label', models.CharField(max_length=30)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='skills/')),
                ('reference', models.URLField()),
                ('label', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+6281255555555'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=80)),
                ('image', models.ImageField(help_text='Rasio harus persegi. Contoh: 600px \xd7 600px', upload_to='certificate/')),
                ('image_label', models.CharField(max_length=50)),
                ('certificate_link', models.URLField()),
                ('certificate_label', models.CharField(max_length=50)),
                ('info_link', models.URLField()),
                ('info_label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=100)),
                ('project_period', models.CharField(max_length=50)),
                ('project_link', models.URLField()),
                ('description', models.TextField()),
                ('image', models.ImageField(help_text='Rasio 1200px \xd7 800px"', upload_to='portfolio/')),
                ('label', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
                ('frameworks', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_access', models.URLField(editable=False)),
                ('ip', models.GenericIPAddressField(editable=False, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('electronic', models.CharField(editable=False, max_length=50)),
                ('is_touchscreen', models.BooleanField(editable=False)),
                ('is_bot', models.BooleanField(editable=False)),
                ('os_type', models.CharField(editable=False, max_length=50)),
                ('os_version', models.CharField(editable=False, max_length=50)),
                ('browser_type', models.CharField(editable=False, max_length=50)),
                ('browser_version', models.CharField(editable=False, max_length=50)),
                ('device_type', models.CharField(editable=False, max_length=50)),
                ('device_brand', models.CharField(editable=False, max_length=50)),
                ('device_model', models.CharField(editable=False, max_length=50)),
                ('username', models.CharField(editable=False, max_length=50)),
                ('country_code', models.CharField(default='NONE', editable=False, max_length=5)),
                ('country', models.CharField(default='None', editable=False, max_length=80)),
                ('region_code', models.CharField(default='NONE', editable=False, max_length=5)),
                ('region', models.CharField(default='None', editable=False, max_length=80)),
                ('city', models.CharField(default='None', editable=False, max_length=80)),
                ('lat', models.DecimalField(decimal_places=4, default=0.0, editable=False, max_digits=8)),
                ('lon', models.DecimalField(decimal_places=4, default=0.0, editable=False, max_digits=8)),
                ('timezone', models.CharField(default='None', editable=False, max_length=20)),
                ('isp', models.CharField(default='None', editable=False, max_length=80)),
                ('isp_detail', models.CharField(default='None', editable=False, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WebEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(editable=False, max_length=50)),
                ('ip', models.GenericIPAddressField(editable=False, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('electronic', models.CharField(editable=False, max_length=50)),
                ('is_touchscreen', models.BooleanField(editable=False)),
                ('is_bot', models.BooleanField(editable=False)),
                ('os_type', models.CharField(editable=False, max_length=50)),
                ('os_version', models.CharField(editable=False, max_length=50)),
                ('browser_type', models.CharField(editable=False, max_length=50)),
                ('browser_version', models.CharField(editable=False, max_length=50)),
                ('device_type', models.CharField(editable=False, max_length=50)),
                ('device_brand', models.CharField(editable=False, max_length=50)),
                ('device_model', models.CharField(editable=False, max_length=50)),
                ('username', models.CharField(editable=False, max_length=50)),
                ('country_code', models.CharField(default='NONE', editable=False, max_length=5)),
                ('country', models.CharField(default='None', editable=False, max_length=80)),
                ('region_code', models.CharField(default='NONE', editable=False, max_length=5)),
                ('region', models.CharField(default='None', editable=False, max_length=80)),
                ('city', models.CharField(default='None', editable=False, max_length=80)),
                ('lat', models.DecimalField(decimal_places=4, default=0.0, editable=False, max_digits=8)),
                ('lon', models.DecimalField(decimal_places=4, default=0.0, editable=False, max_digits=8)),
                ('timezone', models.CharField(default='None', editable=False, max_length=20)),
                ('isp', models.CharField(default='None', editable=False, max_length=80)),
                ('isp_detail', models.CharField(default='None', editable=False, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Web entries',
            },
        ),
        migrations.CreateModel(
            name='YoutubeVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('url', models.URLField()),
            ],
        ),
    ]
