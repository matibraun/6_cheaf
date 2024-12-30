from django.db import migrations
from django.conf import settings

def create_users(apps, schema_editor):

    User = apps.get_model('auth', 'User')
    
    users_data = [
        {'username': 'user1', 'email': 'user1@example.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'user2', 'email': 'user2@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'user3', 'email': 'user3@example.com', 'first_name': 'Alice', 'last_name': 'Johnson'},
        {'username': 'user4', 'email': 'user4@example.com', 'first_name': 'Bob', 'last_name': 'Brown'},
        {'username': 'user5', 'email': 'user5@example.com', 'first_name': 'Charlie', 'last_name': 'Davis'},
        {'username': 'user6', 'email': 'user6@example.com', 'first_name': 'Emily', 'last_name': 'Wilson'},
        {'username': 'user7', 'email': 'user7@example.com', 'first_name': 'Frank', 'last_name': 'Anderson'},
        {'username': 'user8', 'email': 'user8@example.com', 'first_name': 'Grace', 'last_name': 'Taylor'},
        {'username': 'user9', 'email': 'user9@example.com', 'first_name': 'Henry', 'last_name': 'Thomas'},
        {'username': 'user10', 'email': 'user10@example.com', 'first_name': 'Ivy', 'last_name': 'Lee'},
        {'username': 'user11', 'email': 'user11@example.com', 'first_name': 'Jack', 'last_name': 'Moore'},
        {'username': 'user12', 'email': 'user12@example.com', 'first_name': 'Karen', 'last_name': 'Martin'},
        {'username': 'user13', 'email': 'user13@example.com', 'first_name': 'Leo', 'last_name': 'Clark'},
        {'username': 'user14', 'email': 'user14@example.com', 'first_name': 'Mia', 'last_name': 'King'},
        {'username': 'user15', 'email': 'user15@example.com', 'first_name': 'Nathan', 'last_name': 'Scott'},
        {'username': 'user16', 'email': 'user16@example.com', 'first_name': 'Olivia', 'last_name': 'Harris'},
        {'username': 'user17', 'email': 'user17@example.com', 'first_name': 'Peter', 'last_name': 'Martinez'},
        {'username': 'user18', 'email': 'user18@example.com', 'first_name': 'Quinn', 'last_name': 'Robinson'},
        {'username': 'user19', 'email': 'user19@example.com', 'first_name': 'Rachel', 'last_name': 'Walker'},
        {'username': 'user20', 'email': 'user20@example.com', 'first_name': 'Sam', 'last_name': 'Young'},
    ]

    for user_data in users_data:
        User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password='password123'
        )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]