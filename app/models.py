import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

today = date.today()

# Create your models here.

# Manager for Member model (used for tests.py)
class MemberManager(models.Manager):
    def createMember(self, user, height, weight, birth):
        member = self.create(user=user, height=height, weight=weight, birth=birth)
        return member

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.PositiveSmallIntegerField(validators=[MinValueValidator(36)]) # in inches
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(50)]) # in lbs
    birth = models.DateField()

    def ageScore(self):
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
        return (self.ageScore() + self.bmiScore()) * (1 if self.gender == 'M' else 0.85)

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

    # workout preferences (0.0 - 1.0)
    squat = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    lunge = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    reverseLunge = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    jumpSquat = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    lateralLunge = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    calfRaise = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    singleCalfRaise = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    jumpingJack = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    sealJump = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    inwardCalfRaise = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    gluteBridge = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    inchworm = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    goodMorning = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    romanianDeadlift = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    quadLegCurl = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    pushup = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    benchDip = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    pressup = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    plankTap = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    diamondPushup = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    russianTwist = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    situp = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    legRaise = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    deadBug = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    crunchyFrog = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    reverseSnowAngel = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    superman = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    plankRow = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    lowRow = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    latPulldown = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    pullup = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    bicepCurl = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    deadlift = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    benchpress= models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    hammerCurl = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    medicineBallSlam = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    shoulderPress = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    tricepExtension = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    chinup = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    # workout intensity levels (0.0 - 1.0)
    squatDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    lungeDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    reverseLungeDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    jumpSquatDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    lateralLungeDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    calfRaiseDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    singleCalfRaiseDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    jumpingJackDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    sealJumpDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    inwardCalfRaiseDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    gluteBridgeDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    inchwormDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    goodMorningDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    romanianDeadliftDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    quadLegCurlDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    pushupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    benchDipDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    pressupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    plankTapDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    diamondPushupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    russianTwistDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    situpDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    legRaiseDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    deadBugDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    crunchyFrogDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    reverseSnowAngelDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    supermanDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    plankRowDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    lowRowDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    latPulldownDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    pullupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    bicepCurlDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    deadliftDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    benchpressDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    hammerCurlDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    medicineBallSlamDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    shoulderPressDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    tricepExtensionDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    chinupDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    # assigns the django user id to the 'user_id' field for the member in the db
    objects = MemberManager()

class Workout(models.Model):
    #currentUser = get_user_model()

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    workoutDate = models.DateTimeField()
    workoutName = models.CharField(max_length=30)
    steps = models.IntegerField(blank=True, null=True, default=None)
    sets = models.IntegerField(blank=True, null=True, default=None)
    reps = models.IntegerField(blank=True, null=True, default=None)

'''
class User(models.Model):
    # By default, Django creates an auto-incrementing primary key for each model. The
    # following line of code is an alternative way to make a primary key if we don't
    # want to use the default implementation.

    # userID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    password = models.CharField(max_length=30)
    # Duplicate emails not allowed
    email = models.CharField(max_length=50, unique=True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    dateOfBirth = models.DateField()
    weight = models.IntegerField(blank=True)
    accountCreation = models.DateTimeField('date of user\'s registration', auto_now_add=True)

    # A few example of exercise equipment availability checks
    hasDumbbells = models.BooleanField(default=False)
    hasBenchPress = models.BooleanField(default=False)
    hasSquatRack = models.BooleanField(default=False)

    # A few example workout preferences
    squatPreference = models.DecimalField(max_digits=3, decimal_places=2, default=0.50)
    benchpressPreference = models.DecimalField(max_digits=3, decimal_places=2, default=0.50)
    bicepCurlPreference = models.DecimalField(max_digits=3, decimal_places=2, default=0.50)

    # A few example workout intensity levels (assuming a scale of 1-3 for now)
    bicepDifficulty = models.IntegerField(default=2)
    chestDifficulty = models.IntegerField(default=2)
    backDifficulty = models.IntegerField(default=2)

    # It might be a good idea to implement gender for recommendation purposes
    genderChoices = [
    	(M, 'Male'),
    	(F, 'Female'),
    	(N/A, 'Other'),
    ]
    gender = models.CharField(max_length=20, choices=genderChoices, default=N/A)

class Exercise(models.Model):

	# exerciseID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=30)

	# A few examples of exercise equipment
	needsDumbbells = models.BooleanField(default=False)
	needsBenchPress = models.BooleanField(default=False)
	needsSquatRack = models.BooleanField(default=False)

	reps = models.IntegerField('suggested number of repetitions for the average person', default=5)
	sets = models.IntegerField('suggest number of sets for the average person', default=5)

	def __str__(self):
		return self.name

class Workout(models.Model):

	# workoutID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	userID = models.ForeignKey(User, on_delete=models.CASCADE)
	workoutDate = models.DateTimeField()

class CardioWorkout(models.Model):

	# cardioID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	heartRate = models.IntegerField(blank=True)
	steps = models.IntegerField()

	workoutID = models.OneToOneField(Workout, on_delete=models.CASCADE)
	exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

class StrengthWorkout(models.Model):

	# strengthID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	heartRate = models.IntegerField(blank=True)
	sets = models.IntegerField()
	reps = models.IntegerField()

	workoutID = models.OneToOneField(Workout, on_delete=models.CASCADE)
	exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
'''
