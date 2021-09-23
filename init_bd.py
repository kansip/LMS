from django.contrib.auth.models import User

# Создайте пользователя и сохраните его в базе данных
user = User.objects.create_user('Kans', 'test@test.ru', '1234')

# Обновите поля и сохраните их снова
user.first_name = 'John'
user.last_name = 'Citizen'
user.save()

# Создайте пользователя и сохраните его в базе данных
user = User.objects.create_user('admin', 'admin@test.ru', '1234')

# Обновите поля и сохраните их снова
user.first_name = 'ADMIN'
user.last_name = 'ASD'
user.save()