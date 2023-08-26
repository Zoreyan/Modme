# Generated by Django 4.2.4 on 2023-08-24 08:49

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=140, null=True)),
                ('role', models.CharField(choices=[('1', 'Админ'), ('2', 'Студент'), ('3', 'Преподаватель'), ('4', 'Администратор')], default='1', max_length=140, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('content', tinymce.models.HTMLField()),
                ('access', models.BooleanField(blank=True, default=False, null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.course')),
                ('group_access', models.ManyToManyField(blank=True, to='dashboard.group')),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_photos')),
                ('phone', models.CharField(default='996', max_length=12)),
                ('password', models.CharField(default=' ', max_length=20, null=True)),
                ('group', models.ManyToManyField(to='dashboard.group')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pupil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_photos')),
                ('phone', models.CharField(default='996', max_length=12)),
                ('password', models.CharField(default=' ', max_length=20, null=True)),
                ('group', models.ManyToManyField(to='dashboard.group')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(choices=[('vocabulary', 'Vocabulary'), ('grammary', 'Grammary'), ('speaking', 'Speaking'), ('reading', 'Reading'), ('listening', 'Listening')], max_length=80, null=True)),
                ('title', models.CharField(max_length=150, null=True)),
                ('marks', models.PositiveIntegerField(blank=True, null=True)),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('comment', models.TextField(max_length=140)),
                ('created', models.DateField()),
                ('pupil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.pupil')),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_correct_answers', models.IntegerField(null=True)),
                ('total_questions', models.IntegerField(null=True)),
                ('vocabulary_score', models.IntegerField(blank=True, default='0', null=True)),
                ('listening_score', models.IntegerField(blank=True, default='0', null=True)),
                ('reading_score', models.IntegerField(blank=True, default='0', null=True)),
                ('grammary_score', models.IntegerField(blank=True, default='0', null=True)),
                ('speaking_score', models.IntegerField(blank=True, default='0', null=True)),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.lesson')),
                ('pupil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.pupil')),
                ('questions', models.ManyToManyField(to='user.question')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_photos')),
                ('phone', models.CharField(default='996', max_length=12)),
                ('payment', models.IntegerField(null=True)),
                ('password', models.CharField(default=' ', max_length=20, null=True)),
                ('group', models.ManyToManyField(to='dashboard.group')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('price', models.FloatField()),
                ('type', models.CharField(choices=[('plus', 'Приход'), ('minus', 'Расход')], max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('operator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.operator')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.lesson')),
                ('pupils', models.ManyToManyField(to='user.pupil')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, null=True)),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильно')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.question')),
            ],
        ),
    ]