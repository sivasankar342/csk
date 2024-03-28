from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,Permission,Group
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address.'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)  
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)  
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)



    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='%(app_label)s_%(class)s_permissions',  
        help_text=_('Specific permissions for this user.'),
        related_query_name='user',
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='%(app_label)s_%(class)s_groups',  # Adjust this related name
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='user',
    )
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']  
    def str(self):
        return self.user_name