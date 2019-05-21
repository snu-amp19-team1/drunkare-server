from custom_users.models import CustomUser

users = [
    'shpark',
    'parkj0',
    ]

for i,user in enumerate(users):
    CustomUser.objects.create(user_name=user,user_id = i)