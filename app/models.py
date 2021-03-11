import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, datetime

# Create your models here.

# Manager for Member model (used for tests.py)
class MemberManager(models.Manager):
    def createMember(self, user, height, weight, birth):
        member = self.create(user=user, height=height, weight=weight, birth=birth)
        return member

def sane_dates(value):
    if value > timezone.now().date():
        raise ValidationError("Date cannot be in the future.")
    elif value < date(1900, 1, 1):
        raise ValidationError("Date too far in the past.")

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.PositiveSmallIntegerField(validators=[MinValueValidator(36)]) # in inches
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(50)]) # in lbs
    birth = models.DateField(validators=[sane_dates])

    def ageScore(self):
        today = timezone.now().date()
        age = today.year - self.birth.year - ((today.month, today.day) < (self.birth.month, self.birth.day))
        if age <= 8:
            return 1
        elif age <= 14:
            return 5
        elif age <= 18:
            return 7
        elif age <= 25:
            return 11
        elif age <= 35:
            return 8
        elif age <= 50:
            return 5
        elif age <= 65:
            return 4
        elif age <= 80:
            return 2
        else:
            return 1

    def bmiScore(self):
        bmi = (self.weight / pow(self.height, 2)) * 703
        if bmi <= 15.0:
            return 1
        elif bmi <= 18.5:
            return 5
        elif bmi <= 24.9:
            return 9
        elif bmi <= 29.9:
            return 5
        else:
            return 1

    def healthScore(self):
        return (self.ageScore() + self.bmiScore())/2 * (1 if self.gender == 'M' else 0.85)

    GENDER_CHOICES = [
    	('M', 'Male'),
    	('F', 'Female'),
    	('O', 'Other / Prefer not to say'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    FITNESS_GOAL = [
        ('L', 'Lose weight'),
        ('G', 'Gain muscle'),
        ('B', 'Improve general fitness / Both'),
    ]
    goal = models.CharField(max_length=1, choices=FITNESS_GOAL, default='F')

    barbell = models.BooleanField(default=False)
    benchpressEquipment = models.BooleanField(default=False)
    dumbbell = models.BooleanField(default=False)
    pullupBar = models.BooleanField(default=False)
    medicineBall = models.BooleanField(default=False)
    resistanceBand = models.BooleanField(default=False)

    bodyWeight = models.BooleanField(default=True)

    # workout preferences (0.0 - 10.0)
    squat = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    lunge = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    reverseLunge = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    jumpSquat = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    lateralLunge = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    calfRaise = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    singleCalfRaise = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    jumpingJack = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    sealJump = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    inwardCalfRaise = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    gluteBridge = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    inchworm = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    goodMorning = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    romanianDeadlift = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    quadLegCurl = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    pushup = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    benchDip = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    pressup = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    plankTap = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    diamondPushup = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    russianTwist = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    situp = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    legRaise = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    deadBug = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    crunchyFrog = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    reverseSnowAngel = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    superman = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    plankRow = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    lowRow = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    latPulldown = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    pullup = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    bicepCurl = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    deadlift = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    benchpress= models.DecimalField(max_digits=2, decimal_places=1, default=5)
    hammerCurl = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    medicineBallSlam = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    shoulderPress = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    tricepExtension = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    chinup = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    # workout intensity levels (0.0 - 10.0)
    stepDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    
    squatDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    lungeDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    reverseLungeDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    jumpSquatDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    lateralLungeDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    calfRaiseDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    singleCalfRaiseDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    jumpingJackDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    sealJumpDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    inwardCalfRaiseDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    gluteBridgeDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    inchwormDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    goodMorningDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    romanianDeadliftDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    quadLegCurlDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    pushupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    benchDipDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    pressupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    plankTapDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    diamondPushupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    russianTwistDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    situpDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    legRaiseDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    deadBugDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    crunchyFrogDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    reverseSnowAngelDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    supermanDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    plankRowDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    lowRowDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    latPulldownDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    pullupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    bicepCurlDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    deadliftDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    benchpressDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    hammerCurlDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    medicineBallSlamDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    shoulderPressDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    tricepExtensionDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    chinupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=5)

    # the latest exercises that the user was recommended
    baseDate = date(1999, 4, 1)
    latestExerciseRecDate = models.DateField(default=baseDate, validators=[sane_dates])
    latestExerciseRecs = models.CharField(max_length=10000, default="")
    latestStepsRecs = models.IntegerField(default=0)

    # the last date that the user uploaded their data from phone/watch/etc
    latestUploadDate = models.DateField(default=baseDate, validators=[sane_dates])

    # assigns the django user id to the 'user_id' field for the member in the db
    objects = MemberManager()

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    workoutDate = models.DateField(default=timezone.now, validators=[sane_dates])
    steps = models.IntegerField(blank=True, null=True, default=None)
    sets = models.IntegerField(blank=True, null=True, default=None)
    reps = models.IntegerField(blank=True, null=True, default=None)

    WORKOUT_CHOICES = [
        ('squat', 'Squats'),
        ('lunge', 'Lunges'),
        ('reverseLunge', 'Reverse Lunges'),
        ('jumpSquat', 'Jump Squats'),
        ('lateralLunge', 'Lateral Lunges'),
        ('calfRaise', 'Calf Raises'),
        ('singleCalfRaise', 'Single Calf Raises'),
        ('jumpingJack', 'Jumping Jacks'),
        ('sealJump', 'Seal Jumps'),
        ('inwardCalfRaise', 'Inward Calf Raises'),
        ('gluteBridge', 'Glue Bridges'),
        ('inchworm', 'Inchworms'),
        ('goodMorning', 'Good Mornings'),
        ('romanianDeadlift', 'Romanian Dead Lifts'),
        ('quadLegCurl', 'Quad Leg Curls'),
        ('pushup', 'Pushups'),
        ('benchDip', 'Bench Dips'),
        ('pressup', 'Pressups'),
        ('plankTap', 'Plank Taps'),
        ('diamondPushup', 'Diamond Pushups'),
        ('russianTwist', 'Russian Twists'),
        ('situp', 'Situps'),
        ('legRaise', 'Leg Raises'),
        ('deadBug', 'Dead Bugs'),
        ('crunchyFrog', 'Crunchy Frogs'),
        ('reverseSnowAngel', 'Reverse Snow Angels'),
        ('superman', 'Supermans'),
        ('plankRow', 'Plank Rows'),
        ('lowRow', 'Low Rows'),
        ('latPulldown', 'Lat Pulldowns'),
        ('pullup', 'Pullups'),
        ('bicepCurl', 'Bicep Curls'),
        ('deadlift', 'Deadlifts'),
        ('benchpress', 'Benchpress'),
        ('hammerCurl', 'Hammer Curls'),
        ('medicineBallSlam', 'Medicine Ball Slams'),
        ('shoulderPress', 'Shoulder Presses'),
        ('tricepExtension', 'Tricep Extensions'),
        ('chinup', 'Chinups'),]

    workoutName = models.CharField(max_length=30, choices=sorted(WORKOUT_CHOICES), default='step')

    DIFFICULTY_CHOICES = [
        (True, 'Too difficult!'),
        (None, 'Just right!'),
        (False, 'Too easy!'),]
    workoutDifficulty = models.BooleanField(blank=True, choices=DIFFICULTY_CHOICES, default=None, null=True)

    PREFERENCE_CHOICES = [
        (True, 'I liked it!'),
        (None, 'It was okay.'),
        (False, 'I hated it!'),]
    workoutPreference = models.BooleanField(blank=True, choices=PREFERENCE_CHOICES, default=None, null=True)
