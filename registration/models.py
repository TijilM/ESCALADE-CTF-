import uuid
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.db import models
from django.core.validators import RegexValidator
from game.models import Question

# Create your models here.

DISCORD_REGEX = "^.{2,32}#[0-9]{4}$"
EMAIL_REGEX = "^[A-Za-z0-9._~+-]+@thapar\.edu$"
ROLLNO_REGEX = "^[0-9]{9}$"
PHONENO_REGEX = "^[0-9]{10}$"

class Team(AbstractBaseUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamName = models.CharField(max_length=100, unique=True)
    points = models.IntegerField(default=75)
    position = models.IntegerField(default=0)
    board=models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_loggedin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "teamName"
    REQUIRED_FIELDS = []
    
    email = models.EmailField(blank=True)

    current_ques = models.ForeignKey(Question, null=True, blank=True, default=None, on_delete=models.CASCADE)
    dice_value = models.SmallIntegerField(null=True, blank=True, default=None)

    dummy1 = models.CharField(max_length=50, blank=True, null=True, default=None)
    dummy2 = models.CharField(max_length=50, blank=True, null=True, default=None)
    
    level1 = models.CharField(max_length=50, blank=True, default="010203040506070809101112131415")
    level2 = models.CharField(max_length=50, blank=True, default="161718192021222324252627282930")
    level3 = models.CharField(max_length=50, blank=True, default="3132333435363738394041424344454647484950")
    level4 = models.CharField(max_length=50, blank=True, default="5152535455565758596061626364656667686970")

    hint_taken = models.BooleanField(blank=True, default=False)
    sneakpeek_taken = models.CharField(max_length=10, null=True, blank=True, default=None)

    def get_short_name(self):
        # The user is identified by their team name
        return self.teamName

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def __str__(self):
        return self.teamName


class Participant(models.Model):
    name = models.CharField(max_length=50)
    
    roll_no = models.CharField(
        max_length=9,
        unique=True,
        validators=[
            RegexValidator(
                regex=ROLLNO_REGEX,
                message='Invalid Roll Number',
                code='invalid_rollno'
            )
        ],
    )

    phone_no = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=PHONENO_REGEX,
                message='Invalid Phone Number',
                code='invalid_phoneno'
            )
        ],
    )
    
    email = models.EmailField(
        unique=True,
        validators=[
            RegexValidator(
                regex=EMAIL_REGEX,
                message='Invalid email address',
                code='invalid_email'
            )
        ],
    )
    
    discord_ID = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex=DISCORD_REGEX,
                message="Invalid Discord ID",
                code="invalid_discordID"
            )
        ],
    )
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True)

    
