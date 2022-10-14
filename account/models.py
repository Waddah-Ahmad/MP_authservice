from tokenize import group
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


#  Custom User Manager
class UserManager(BaseUserManager):

  def create_user(self, email, name, tc , password=None, password2=None):

      """
      Creates and saves a User with the given email, name and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
      )
      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name,  password=None):
    """
    Creates and saves a superuser with the given email, name, tc and password.
    """
    user = self.create_user(
        email,
        password=password,
        name=name,

        tc=tc,
        

    )
    user.group = "admin"
    user.is_admin = True
    user.is_streamer = True
    user.group = "admin"
    user.save(using=self._db)
    return user

  def create_streamer(self, email, name, password=None, password2=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')
      user = self.model(
          email=self.normalize_email(email),
          name=name,
      )
      user.group = "streamer"
      user.set_password(password)
      user.is_admin = False
      user.is_streamer = True
      user.group = "streamer"
      user.save(using=self._db)
      return user


#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  group = models.CharField(max_length=200 ,default="user")
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  is_streamer = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  group= models.CharField(max_length=50, default="user")

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc' ]

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin





