from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class FileSystem(MPTTModel):
	name = models.CharField(max_length=200, unique=True,)
	parent = TreeForeignKey("self",on_delete=models.CASCADE, null=True, blank=True,related_name="children")

	class MPTTMeta:
		order_insertion_by = ["name"]


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, display_name, password=None):
		if not email:
			raise ValueError("Users must have an email")
		if not username:
			raise ValueError("User must have username")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			display_name=display_name
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, display_name, email, password):
		user = self.create_user(
			email=self.normalize_email(email),
			display_name=display_name,
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	homepage = models.URLField(null=True, blank=True)
	display_name = models.CharField(max_length=25, unique=True)
	email = models.EmailField(verbose_name='email', max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'display_name']

	objects = MyAccountManager()

	def __str__(self):
		return self.display_name

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


def __str__(self):
	return self.name


