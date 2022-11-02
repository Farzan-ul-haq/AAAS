from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        """Create and saves a new User"""
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """Creates and saves a new super user"""
        user = self.create_user(
            username, 
            password, 
            email=username+'@gmail.com',
            is_staff=True,
            is_superuser=True
        )
        return user