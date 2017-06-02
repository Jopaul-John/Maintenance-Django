from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.template.defaultfilters import slugify
from django.utils import timezone


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# TODO: virus check flag, 3 level permission: student, staff, admin, add complaint ID


class DeviceManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super().all(*args, **kwargs).filter(is_active=True)
        return qs


class Device(models.Model):
    LAB_CHOICES = (
        ('Lab-1', 'Lab 1'),
        ('Lab-5', 'Lab 5'),
        ('CCF', 'CCF'),
    )

    objects = DeviceManager()

    buy_date = models.DateField(blank=True)
    image = models.URLField(blank=True)
    model = models.CharField(max_length=100, blank=False)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    device_id = models.CharField(max_length=50, blank=True, unique=True)
    description = models.CharField(max_length=150, blank=True)
    vendor_info = models.CharField(max_length=150, blank=True)
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)   # Set to false instead of deleting
    last_check = models.DateField(blank=True)
    issues_count = models.IntegerField(default=0)
    buy_price = models.IntegerField(null=True)
    current_price = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('auth.User', related_name='devices', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.device_id, self.model)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.model+' '+self.device_id)
            self.last_check = self.buy_date
            self.current_price = self.buy_price
        super().save(*args, **kwargs)


class DeviceHistory(models.Model):
    # complaint_id = models.IntegerField()
    date = models.DateField()
    issue = models.CharField(max_length=500)
    image = models.ImageField(blank=True, null=True)
    device = models.ForeignKey(Device, related_name='history', on_delete=models.CASCADE)
    resolved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device.device_id

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.device.issues_count += 1
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=True)
    is_lab_staff = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)


class Location(models.Model):
    name = models.CharField(max_length=50, help_text="Please enter value slugified. Eg: lab-04, CCF")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
