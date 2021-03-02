import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.PositiveSmallIntegerField(validators=[MinValueValidator(36)]) # in inches
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(50)]) # in lbs
    birth = models.DateField()

    GENDER_CHOICES = [
    	('M', 'Male'),
    	('F', 'Female'),
    	('O', 'Other / Prefer not to say'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    FITNESS_GOAL = [
        ('L', 'Lose weight'),
        ('G', 'Gain muscle'),
        ('F', 'Improve general fitness / Both'),
    ]
    goal = models.CharField(max_length=1, choices=FITNESS_GOAL, default='F')

    barbell = models.BooleanField(default=False)
    dumbbell = models.BooleanField(default=False)
    pullup_bar = models.BooleanField(default=False)
    resistance_band = models.BooleanField(default=False)
    bench = models.BooleanField(default=False)
    medicine_ball = models.BooleanField(default=False)




    # A few example workout preferences (0.0 - 1.0)
    #squatPreference = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    #benchpressPreference = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    #bicepCurlPreference = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

    # A few example workout intensity levels (assuming a scale of 1-3 for now)
    #bicepDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    #chestDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)
    #backDifficulty = models.DecimalField(max_digits=2, decimal_places=1, default=0.5)

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
