from django.db import migrations, models
from django.contrib.auth.hashers import make_password

def prepopulate_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    predefined_usernames = ['hardik', 'aryan', 'harish', 'rasika']
    for username in predefined_usernames:
        if not User.objects.filter(username=username).exists():
            User.objects.create(
                username=username,
                email=f"{username}@example.com",
                password=make_password('password123'),
                is_active=True,
                is_staff=False,
                is_superuser=False
            )

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='due_date',
        ),
        migrations.AddField(
            model_name='task',
            name='story_points',
            field=models.IntegerField(blank=True, null=True, verbose_name='Story Points'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('to_do', 'To Do'), ('in_progress', 'In Progress'), ('in_review', 'In Review'), ('done', 'Done')], default='to_do', max_length=50, verbose_name='Status'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.RunPython(prepopulate_users),
    ]
