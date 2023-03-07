from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse


class MyAccountManager(BaseUserManager):
    def create_user(self, fname, lname, email, phone_number, is_staff, is_user, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not lname:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            lname=lname,
            fname=fname,
            phone_number=phone_number,
            is_user=is_user,
            is_staff=is_staff,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fname, email, lname, password, phone_number):
        user = self.create_user(
            email=self.normalize_email(email),
            fname=fname,
            password=password,
            lname=lname,
            phone_number=phone_number,

        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_user = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


role_choices = (('customer', 'customer'), ('seller', 'seller'), ('None', 'None'))


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100, blank=True, null=True)
    lname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.BigIntegerField(default=0)
    roles = models.CharField(max_length=100, choices=role_choices, default="")

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    approved_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'phone_number', ]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    descripton = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('antiqueapp:products_by_category', args=self.slug)

    def __str__(self):
        return '{}'.format(self.name)


class product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    descripton = models.TextField(blank=True)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField(default=1)
    image = models.ImageField()
    availabe = models.BooleanField(default=True)
    createf = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return '{}'.format(self.name)
