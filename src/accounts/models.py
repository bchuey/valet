from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    # drivers_license = generic.GenericRelation('DriversLicense')
    is_available = models.BooleanField(default=False)

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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_valet_is_available(sender, instance, created, *args, **kwargs):

    if created:
        instance.is_available = True
        instance.save()




# class Valet(User):

#     is_valet = models.BooleanField(default=True)
#     is_available = models.BooleanField(default=True)
#     drivers_license = GenericRelation('DriversLicense')
#     class Meta:

#         db_table = 'valets'

#     def __unicode__(self):

#         return unicode(self.email)

#     def __str__(self):

#         return self.email





PARKING_ZONES = (

    ('A','A'),
    ('B','B'),
    ('BB','BB'),
    ('C','C'),
    ('CC','CC'),
    ('D','D'),
    ('DD','DD'),
    ('E','E'),
    ('F','F'),
    ('G','G'),
    ('H','H'),
    ('I','I'),
    ('J','J'),
    ('K','K'),
    ('L','L'),
    ('M','M'),
    ('N','N'),
    ('O','O'),
    ('P','P'),
    ('Q','Q'),
    ('R','R'),
    ('S','S'),
    ('T','T'),
    ('U','U'),
    ('V','V'),
    ('W','W'),
    ('X','X'),
    ('Y','Y'),
    ('Z','Z'),
)


class RegisteredVehicle(models.Model):
    owned_by = models.ForeignKey(User, related_name='registered_vehicle')
    make = models.CharField(max_length=60) # could be a dropdown list
    model = models.CharField(max_length=60)
    color = models.CharField(max_length=60)
    year = models.CharField(max_length=4,null=True,blank=True)
    license_plate_number = models.CharField(max_length=10)
    updated_registration_tags = models.BooleanField(default=True)
    parking_permit_zone = models.CharField(max_length=2, choices=PARKING_ZONES, blank=True)

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

"""
Using ContentType framework to create relationship between both User and Valet
"""
# class DriversLicense(models.Model):
#     # owned_by = models.ForeignKey(User)
#     legal_first_name = models.CharField(max_length=60)
#     legal_last_name = models.CharField(max_length=60)
#     date_of_birth = models.DateField()
#     license_id_number = models.CharField(max_length=60)
#     registered_city = models.CharField(max_length=100)
#     registered_state = models.CharField(max_length=25)
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForiegnKey()

#     class Meta:

#         db_table = 'driver_licenses'

#     def __unicode__(self):

#         return self.license_id_number

#     def __str__(self):

#         return self.license_id_number



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