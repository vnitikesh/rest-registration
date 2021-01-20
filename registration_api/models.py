from django.db import models, transaction
import datetime
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
import re
from django.utils.crypto import get_random_string

# Create your models here.

User = get_user_model()
token_generator = default_token_generator
SHA1_RE = re.compile('^[a-f0-9]{40}$')

class TimeStampModel(models.Model):
    timestamp_created = models.DateTimeField(auto_now_add = True)
    timestamp_updated = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


class Verification(models.Model):
    has_email_verified = models.BooleanField(default = False)

    class Meta:
        abstract = True



class RegistrationProfileManager(models.Manager):

    @transaction.atomic
    def create_user_profile(self, data, is_active = False, site = None, send_email = True):
        password = data.pop('password')
        user = User(**data)
        user.is_active = is_active
        user.set_password(password)
        user.save()

        user_profile = self.create_profile(user)

        if(send_email):
            user_profile.send_activation_email(site)
        return user

    def create_profile(self, user):
        username = str(getattr(user, User.USERNAME_FIELD))
        hash_input = (get_random_string(5) + username).encode('utf-8')
        verification_key = hashlib.sha1(hash_input).hexdigest()

        profile = self.create(user = user, verification_key = verification_key)
        return profile


    def activate_user(self, verification_key):
         if SHA1_RE.search(verification_key.lower()):
            try:
                user_profile = self.get(verification_key=verification_key)
            except ObjectDoesNotExist:
                return None
            if not user_profile.verification_key_expired():
                user = user_profile.user
                user.is_active = True
                user.save()
                user_profile.verification_key = RegistrationProfile.ACTIVATED
                user_profile.has_email_verified = True
                user_profile.save()
                return user
         return None



class RegistrationProfile(TimeStampModel, Verification):

    ACTIVATED = "ALREADY ACTIVATED"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, unique = True, verbose_name = ugettext_lazy('user'), related_name = 'api_registration_profile')
    verification_key = models.CharField(ugettext_lazy('activation_key'), max_length = 40)
    objects = RegistrationProfileManager()

    class Meta:
        verbose_name = u'user profile'
        verbose_name_plural = u'user profiles'

    def __str__(self):
        return str(self.user)

    def verification_key_expired(self):
        expiration_date = datetime.timedelta(days = getattr(settings, 'VERIFICATION_KEY_EXPIRY_DAYS', 2))
        return self.verification_key == self.ACTIVATED or (self.user.date_joined + expiration_date <= timezone.now())


    def send_activation_email(self, site):
        context = {
            'verification_key': self.verification_key,
            'expiry_days': getattr(settings, 'VERIFICATION_KEY_EXPIRY_DAYS',2),
            'user': self.user,
            'site': site,
            #'site_name': getattr(settings, 'SITE_NAME', None)

        }


        subject = render_to_string('registration/activation_email_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string('registration/activation_email_content.txt', context)

        msg = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [self.user.email])
        msg.attach_alternative(message, "text/html")
        msg.send()
