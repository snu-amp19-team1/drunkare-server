cat db_init/clear_data.py | python manage.py shell
cat db_init/init_activity.py | python manage.py shell
cat db_init/init_context.py | python manage.py shell
cat db_init/init_user.py | python manage.py shell

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'drunkare!@#$ ')" | python manage.py shell