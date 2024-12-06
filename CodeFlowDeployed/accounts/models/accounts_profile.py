from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from CodeFlowDeployed.validators import NameLetterValidator, ImageSizeValidator
from cloudinary.models import CloudinaryField



UserModel = get_user_model()

class Profile(models.Model):
    MIN_LEN_NAME = 2
    MAX_LEN_NAME = 30
    MAX_IMAGE_SIZE = 5
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        validators=[
            MinLengthValidator(MIN_LEN_NAME),
            NameLetterValidator()
        ],
        max_length=MAX_LEN_NAME,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        validators=[
            MinLengthValidator(MIN_LEN_NAME),
            NameLetterValidator()
        ],
        max_length=MAX_LEN_NAME,
        blank=True,
        null=True,
    )

    profile_picture = CloudinaryField(
        'image',
        blank=True,
        null=True,
        validators=[ImageSizeValidator(MAX_IMAGE_SIZE)],
    )


    def get_full_name(self):
        if self.first_name is not None and self.last_name is not None:
            return self.first_name + " " + self.last_name

        return self.first_name or self.last_name or "No name given."

    def save(self, *args, **kwargs):
        if self.first_name in ["", "None"]:
            self.first_name = None
        if self.last_name in ["", "None"]:
            self.last_name = None
        super().save(*args, **kwargs)