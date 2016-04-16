from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from accounts.managers import UserManager

def upload_to(instance, filename):

    url = 'accounts/{full_name}/profile_pic/{filename}'.format(full_name=instance.get_media_directory(),filename=filename)

    return url

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_valet = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to=upload_to, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth','first_name','last_name']

    class Meta:

    	db_table = 'accounts'

    def get_full_name(self):
        # The user is identified by their email address
        # return self.email
        full_name = '{first} {last}'.format(first=self.first_name,last=self.last_name)

        return full_name

    def get_media_directory(self):

        folder_name = '{first}_{last}'.format(first=self.first_name,last=self.last_name)

        return folder_name


    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class RegisteredVehicle(models.Model):
    owned_by = models.ForeignKey(User)
    make = models.CharField(max_length=60) # could be a dropdown list
    model = models.CharField(max_length=60)
    color = models.CharField(max_length=60)
    year = models.CharField(max_length=4,null=True,blank=True)
    license_plate_number = models.CharField(max_length=10)
    updated_registration_tags = models.BooleanField(default=True)

    class Meta:

        db_table = 'registered_vehicles'

    def __unicode__(self):

        return self.license_plate_number

    def __str__(self):

        return self.license_plate_number


class DriversLicense(models.Model):
    owned_by = models.ForeignKey(User)
    legal_first_name = models.CharField(max_length=60)
    legal_last_name = models.CharField(max_length=60)
    date_of_birth = models.DateField()
    license_id_number = models.CharField(max_length=60)
    registered_city = models.CharField(max_length=100)
    registered_state = models.CharField(max_length=25)

    class Meta:

        db_table = 'driver_licenses'

    def __unicode__(self):

        return self.license_id_number

    def __str__(self):

        return self.license_id_number


class InsurancePolicy(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    insured_vehicle = models.ForeignKey(RegisteredVehicle, null=True, blank=True)
    company = models.CharField(max_length=30)
    policy_number = models.CharField(max_length=50)
    agent_first_name = models.CharField(max_length=25)
    agent_last_name = models.CharField(max_length=25)
    agent_phone_number = models.CharField(max_length=10)

    class Meta:

        db_table = 'insurance_policies'

    def __unicode__(self):

        return self.policy_number

    def __str__(self):

        return self.policy_number