#from .models import Member
import datetime
import pandas as pd
import random
from .models import MemberManager, Member
from django.contrib.auth.models import User
import json

# TODO: sync this with models.py
WORKOUT_CHOICES = {
    'squat': 'Squats',
    'lunge': 'Lunges',
    'reverseLunge': 'Reverse Lunges',
    'jumpSquat': 'Jump Squats',
    'lateralLunge': 'Lateral Lunges',
    'calfRaise': 'Calf Raises',
    'singleCalfRaise': 'Single Calf Raises',
    'jumpingJack': 'Jumping Jacks',
    'sealJump': 'Seal Jumps',
    'inwardCalfRaise': 'Inward Calf Raises',
    'gluteBridge': 'Glute Bridges',
    'inchworm': 'Inchworms',
    'goodMorning': 'Good Mornings',
    'romanianDeadlift': 'Romanian Dead Lifts',
    'quadLegCurl': 'Quad Leg Curls',
    'pushup': 'Pushups',
    'benchDip': 'Bench Dips',
    'pressup': 'Pressups',
    'plankTap': 'Plank Taps',
    'diamondPushup': 'Diamond Pushups',
    'russianTwist': 'Russian Twists',
    'situp': 'Situps',
    'legRaise': 'Leg Raises',
    'deadBug': 'Dead Bugs',
    'crunchyFrog': 'Crunchy Frogs',
    'reverseSnowAngel': 'Reverse Snow Angels',
    'superman': 'Supermans',
    'plankRow': 'Plank Rows',
    'lowRow': 'Low Rows',
    'latPulldown': 'Lat Pulldowns',
    'pullup': 'Pullups',
    'bicepCurl': 'Bicep Curls',
    'deadlift': 'Deadlifts',
    'benchpress': 'Benchpress',
    'hammerCurl': 'Hammer Curls',
    'medicineBallSlam': 'Medicine Ball Slams',
    'shoulderPress': 'Shoulder Presses',
    'tricepExtension': 'Tricep Extensions',
    'chinup': 'Chinups',
}


class Exercise:
    def __init__(self, name, sets, reps, video_link, eqp_list):
        self.name = WORKOUT_CHOICES[name]
        self.combination = str(sets) + 'x' + str(reps)
        self.embed = video_link
        self.requires = eqp_list


class Recommendation:
    def __init__(self, request):
        # get the user from the models
        if request.user.is_authenticated:
            self.user = Member.objects.get(user=request.user.id)
            print("AUTHENTICATED")
        else:
            print("UNAUTHENTICATED")

        input_path = './app/exercises.csv'
        steps_path = './app/steps.csv'

        self.health_score = self.user.healthScore()
        # list of all the exercises
        self.df = pd.read_csv(input_path)
        self.steps_df = pd.read_csv(steps_path)

        # equipment that the user has
        self.user_eqp = ['bodyweight']

        # user's pref for all the exercises that exist
        self.pref_list = []

        # all the valid exercises that exist
        self.all_exercise_id_list = []
        self.all_exercise_name_list = []

        # ids of the exercises that the user is recommended
        self.exercise_recs_id = []
        self.exercise_recs_name = []

        # list of scores per exercise that user is recommended
        self.overall_score = []

        # list of the recommended sets and reps, video links, and equipment for all recommended exercises
        self.final_recs = []
        self.step_rec = 0

        # list of exercises gets stored to database
        self.exerciseListToDb = []

    def get_valid_equipment(self):
        # returns list of valid equipment based on what the user owns
        if self.user.barbell:
            self.user_eqp.append('barbell')
        if self.user.dumbbell:
            self.user_eqp.append('dumbbell')
        if self.user.pullupBar:
            self.user_eqp.append('pullup bar')
        if self.user.resistanceBand:
            self.user_eqp.append('resistance band')
        if self.user.benchpressEquipment:
            self.user_eqp.append('bench')
        if self.user.medicineBall:
            self.user_eqp.append('medicine ball')

    def find_exercise_pref(self, exercise):
        # find exercise preference in the model
        return getattr(self.user, exercise)
    
    def fill_preferences(self):
        # TODO: for current user
        # returns list of preference weight corresponding to the exercise list
        self.pref_list = []
        for exercise in self.all_exercise_name_list:
            self.pref_list.append(float(self.find_exercise_pref(exercise)))
    
    def get_valid_exercises(self, muscle):
        # returns list of valid exercises based on the target muscle and equipment list
        # self.all_exercise_id_list = []
        # self.all_exercise_name_list = []
        for eqp in self.user_eqp:
            for index, row in self.df.loc[(self.df['muscle'] == muscle) & (self.df[eqp])].iterrows():
                if row['id'] not in self.all_exercise_id_list:
                    self.all_exercise_id_list.append(row['id'])
                    self.all_exercise_name_list.append(row['exercise'])

        # return (self.all_exercise_id_list, self.all_exercise_name_list)

    def make_exercise_rec(self, muscle_list):
        # returns list of exercises that we recommend the user based off their preferences

        for muscle in muscle_list:
            self.get_valid_exercises(muscle)
            self.fill_preferences()

            choices = random.choices(population=self.all_exercise_id_list, weights=self.pref_list, k=50)

            counter = 0
            i = 0
            while i < len(choices) and counter < 2:
                if choices[i] not in self.exercise_recs_id:
                    self.exercise_recs_id.append(choices[i])
                    self.exercise_recs_name.append(self.df.loc[(self.df['id'] == choices[i])]['exercise'].unique()[0])
                
                    counter += 1
                print(self.exercise_recs_id)
                print(self.exercise_recs_name)
                i += 1


    def find_exercise_diff(self, exercise):
        # find exercise difficulty in the model
        return getattr(self.user, exercise + 'Difficulty')
        # return 1
    
    def fill_difficulty(self):
        # TODO: for current user
        # returns list of overall scores corresponding to the exercises they are recommended
        for exercise in self.exercise_recs_name:
            self.overall_score.append(self.user.healthScore() * float(self.find_exercise_diff(exercise)))

    def get_sets_reps(self):
        # returns dict of {id: {sets, reps}} based off the overall difficulty for
        # each exercise
        final_recs = set()

        for i in range(len(self.exercise_recs_id)):
            for index, row in self.df.loc[(self.df['id'] == self.exercise_recs_id[i]) & (self.df['overallMin'] <= self.overall_score[i]) & (
                    self.overall_score[i] <= self.df['overallMax'])].iterrows():
                print("final_recs", final_recs)
                print("row", row)
                if row['exercise'] not in final_recs:
                    print('row[exercise]',row['exercise'])
                    optional_eqp = []
                    for eqp in self.user_eqp:
                        if row[eqp]:
                            optional_eqp.append(eqp)

                    # adds the dictionary to a list that will be saved to the database storing the exercises recommended to the user
                    tempDict = {"exercise": row['exercise'], "sets":row['sets'], "reps": row['reps'], "embed": row['video link'], "eqp_list": optional_eqp}
                    self.exerciseListToDb.append(tempDict)

                    ex = Exercise(row['exercise'], row['sets'], row['reps'], row['video link'], optional_eqp)
                    final_recs.add(row['exercise'])
                    self.final_recs.append(ex)
    
    def make_steps_rec(self):
        overall_step_score = self.health_score * float(self.user.stepDifficulty)
        self.step_rec = int(self.steps_df.loc[(self.steps_df['difficultyMin'] <= overall_step_score) & \
            (self.steps_df['difficultyMax'] >= overall_step_score)]['stepCount'])

    def get_muscle_groups(self):
       
        # get todays day of week, monday is 0 sunday is 6
        weekday = datetime.datetime.today().weekday()

        print("Goal: ", self.user.goal, "Weekday: ", weekday)
        # if users goal is lose weight, less exercise days
        # recommend legs, core mon
        # recommend arms, back fri
        muscle_list = []
        if self.user.goal == 'L':
            if weekday == 0:
                muscle_list = ['quadricep', 'calf', 'hamstring', 'core']
            elif weekday == 1:
                pass
            elif weekday == 2:
                pass
            elif weekday == 3:
                pass
            elif weekday == 4:
                muscle_list = ['bicep', 'tricep', 'back']
            elif weekday == 5:
                pass
            elif weekday == 6:
                pass


        # if users goal is gain muscle, more exercise days
        # recommend quads, hamstring mon
        # recommend bicep, tricep wed
        # recommend calf, core fri
        # recommend back sun
        elif self.user.goal == 'G':
            if weekday == 0:
                muscle_list = ['quadricep', 'hamstring']
            elif weekday == 1:
                pass
            elif weekday == 2:
                muscle_list = ['bicep', 'tricep']
            elif weekday == 3:
                pass
            elif weekday == 4:
                muscle_list = ['calf', 'core']
            elif weekday == 5:
                pass
            elif weekday == 6:
                muscle_list = ['back']



        # if users goal is general, 3 exercise days
        # recommend quads, calf, hamstring mon
        # recommend bicep, tricep  wed
        # recommend core, back sat
        elif self.user.goal == 'B':
            if weekday == 0:
                muscle_list = ['quadricep', 'calf', 'hamstring']
            elif weekday == 1:
                pass
            elif weekday == 2:
                muscle_list = ['bicep', 'tricep']
            elif weekday == 3:
                pass
            elif weekday == 4:
                muscle_list = ['back', 'core']
            elif weekday == 5:
                muscle_list = ['quadricep', 'calf', 'hamstring']
            elif weekday == 6:
                pass
        
        return muscle_list

    def ex_from_dict(self, exercise_dict):

        for ex in exercise_dict:
            e = Exercise(ex['exercise'], ex['sets'], ex['reps'], ex['embed'], ex['eqp_list'])
            self.final_recs.append(e)


    def make_recommendations(self):

        # self.user.latestExerciseRecDate = datetime.date(2020,3,3)
        if (self.user.latestExerciseRecDate == datetime.date.today()):
            print('latestExerciseRecs', self.user.latestExerciseRecs)
            exercise_dict = json.loads(self.user.latestExerciseRecs)
            print('exercise_dict', exercise_dict)
            self.ex_from_dict(exercise_dict)
            self.step_rec = self.user.latestStepsRecs
            print('self.final_recs',self.final_recs)

        

        else:
            # store the equipment that the user has
            self.get_valid_equipment()
            print("health: ", self.health_score, "stepDifficulty: ", self.user.stepDifficulty)
            # get the list of muscles that have to be worked out (or empty list if none have to be worked out)
            muscle_list = self.get_muscle_groups()
            print("muscle list: ", muscle_list)
            self.make_exercise_rec(muscle_list)
            self.make_steps_rec()
            if not muscle_list:
                self.step_rec += 500
            
            print("steps: ", self.step_rec)

            self.fill_difficulty()
            print('final_recs',self.final_recs)
            print('get_sets_reps()',self.get_sets_reps())
            print('final_recs',self.final_recs)

            self.user.latestExerciseRecDate = datetime.date.today()
            self.user.latestExerciseRecs = json.dumps(self.exerciseListToDb)
            self.user.latestStepsRecs = self.step_rec
            self.user.save()