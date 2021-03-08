#from .models import Member
import datetime
import pandas as pd
import random
from .models import MemberManager, Member
from django.contrib.auth.models import User

class Exercise:
    def __init__(self, name, sets, reps, video_link, eqp_list):
        self.name = name
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

        # list of all the exercises
        self.df = pd.read_csv(input_path)

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
                    self.exercise_recs_name.append(self.df.loc[(self.df['id'] == choices[i])]['exercise'].unique())
                
                    counter += 1
                print(self.exercise_recs_id)
                print(self.exercise_recs_name)
                i += 1


    def find_exercise_diff(self, exercise):
        # find exercise difficulty in the model
        return getattr(self.user, exercise + 'Difficulty')
    
    def fill_difficulty(self):
        # TODO: for current user
        # returns list of overall scores corresponding to the exercises they are recommended
        for exercise in self.exercise_recs_id:
            self.overall_score.append(self.user.healthScore() * find_exercise_diff(exercise))

    def get_sets_reps(self):
        # returns dict of {id: {sets, reps}} based off the overall difficulty for
        # each exercise

        for i in range(len(self.exercise_recs_id)):
            for index, row in self.df.loc[(self.df['id'] == self.exercise_recs_id[i]) & (self.df['overallMin'] < self.overall_score[i]) & (
                    self.overall_score[i] < self.df['overallMax'])].iterrows():
                optional_eqp = []
                for eqp in self.user_eqp:
                    if row[eqp]:
                        optional_eqp.append(eqp)

                ex = Exercise(row['exercise'], row['sets'], row['reps'], row['video link'], optional_eqp)
                self.final_recs.append(ex)
    
    def make_recommendations(self):
        
        # get todays day of week, monday is 0 sunday is 6
        weekday = datetime.datetime.today().weekday()

        self.make_exercise_rec(['calf', 'hamstring'])

        self.fill_difficulty()
        print(self.final_recs)
        print(self.get_sets_reps())
        print(self.final_recs)

"""
    valid_equipment = get_valid_equipment(curr_user)
    # if users goal is lose weight, less exercise days
    # recommend legs, core mon
    # recommend arms, back fri
    if curr_user.goal == 'L':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'calf', 'hamstring', 'core'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            pass
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep', 'back'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            pass


    # if users goal is gain muscle, more exercise days
    # recommend quads, hamstring mon
    # recommend bicep, tricep wed
    # recommend calf, core fri
    # recommend back sun
    elif curr_user.goal == 'G':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'hamstring'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep'], valid_equipment)
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['calf', 'core'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            final_exercises = make_exercise_rec(df, ['back'], valid_equipment)



    # if users goal is general, 3 exercise days
    # recommend quads, calf, hamstring mon
    # recommend bicep, tricep  wed
    # recommend core, back sat
    elif curr_user.goal == 'F':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'calf', 'hamstring'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep'], valid_equipment)
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['back', 'core'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            pass



def get_valid_equipment(user):
    # returns list of valid equipment based on what the user owns
    available_eqp = ['bodyweight']
    if user.barbell:
        available_eqp.append('barbell')
    if user.dumbbell:
        available_eqp.append('dumbbell')
    if user.pullupBar:
        available_eqp.append('pullup bar')
    if user.resistanceBand:
        available_eqp.append('resistance band')
    if user.benchpressEquipment:
        available_eqp.append('bench')
    if user.medicineBall:
        available_eqp.append('medicine ball')

    return available_eqp


def find_exercise_pref(curr_user, exercise):
    # find exercise preference in the model
    return getattr(curr_user, exercise)

def find_exercise_diff(exercise):
    # find exercise difficulty in the model
    return 1


def get_valid_exercises(df, muscle, equipment_list):
    # returns list of valid exercises based on the target muscle and equipment list
    exercise_id_set = set()
    exercise_name_set = set()
    for eqp in equipment_list:
        for row in df.loc[(df['muscle'] == muscle) & (df[eqp])]['id'].unique():
            exercise_id_set.add(row)
        for row in df.loc[(df['muscle'] == muscle) & (df[eqp])]['exercise'].unique():
            exercise_name_set.add(row)

    return (list(exercise_set), list(exercise_name_set))


def fill_preferences(curr_user, exercises_list):
    # TODO: for current user
    # returns list of preference weight corresponding to the exercise list
    weight_list = []
    for exercise in exercises_list:
        weight_list.append(find_exercise_pref(curr_user, exercise))
    return weight_list


def fill_difficulty(health_score, exercises_list):
    # TODO: for current user
    # returns list of difficulty weight corresponding to the exercise list
    weight_list = []
    for exercise in exercises_list:
        weight_list.append(health_score * find_exercise_diff(exercise))
    return weight_list


def make_exercise_rec(df, muscle_list, equipment_list, curr_user):
    # returns list of exercises that we recommend the user based off their preferences
    final_recs = set()
    for muscle in muscle_list:
        exercises = get_valid_exercises(df, muscle, equipment_list)
        print(muscle, exercises)
        prefs = fill_preferences(curr_user, exercises)
        choices = random.choices(population=exercises, weights=prefs, k=50)

        counter = 0
        i = 0
        while i < len(choices) and counter < 2:
            if choices[i] not in final_recs:
                final_recs.add(choices[i])
                counter += 1
            i += 1
    return list(final_recs)


def get_sets_reps(df, final_exercises, overall_diff):
    # returns dict of {id: {sets, reps}} based off the overall difficulty for
    # each exercise
    out = {}
    print(df.loc[(df['id'] == 1)]['overallMax'])

    for i in range(len(final_exercises)):
        for index, row in df.loc[(df['id'] == final_exercises[i]) & (df['overallMin'] < overall_diff) & (
                    overall_diff < df['overallMax'])].iterrows():
            out[final_exercises[i]] = {}
            out[final_exercises[i]]['sets'] = row['sets']
            out[final_exercises[i]]['reps'] = row['reps']
    return out

def make_recommendations(curr_user):
    # returns dict of exercies with sets and reps
    # TODO: consider user and day of week
    # need this for when running from python3 manage.py runserver
    input_path = './app/exercises.csv'
    # otherwise working directory is app
    # input_path = '../app/exercises.csv'

    df = pd.read_csv(input_path)
    print(df)

    # get todays day of week, monday is 0 sunday is 6
    weekday = datetime.datetime.today().weekday()

    final_exercises = make_exercise_rec(df, ['calf', 'hamstring'], ["bodyweight", "barbell"], curr_user)
    print(final_exercises)
    overall_diff = find_exercise_diff(final_exercises)
    print(get_sets_reps(df, final_exercises, overall_diff))


    print(final_exercises)
"""
    valid_equipment = get_valid_equipment(curr_user)
    # if users goal is lose weight, less exercise days
    # recommend legs, core mon
    # recommend arms, back fri
    if curr_user.goal == 'L':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'calf', 'hamstring', 'core'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            pass
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep', 'back'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            pass


    # if users goal is gain muscle, more exercise days
    # recommend quads, hamstring mon
    # recommend bicep, tricep wed
    # recommend calf, core fri
    # recommend back sun
    elif curr_user.goal == 'G':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'hamstring'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep'], valid_equipment)
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['calf', 'core'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            final_exercises = make_exercise_rec(df, ['back'], valid_equipment)



    # if users goal is general, 3 exercise days
    # recommend quads, calf, hamstring mon
    # recommend bicep, tricep  wed
    # recommend core, back sat
    elif curr_user.goal == 'F':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'calf', 'hamstring'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep'], valid_equipment)
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['back', 'core'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            pass



def get_valid_equipment(user):
    # returns list of valid equipment based on what the user owns
    available_eqp = ['bodyweight']
    if user.barbell:
        available_eqp.append('barbell')
    if user.dumbbell:
        available_eqp.append('dumbbell')
    if user.pullupBar:
        available_eqp.append('pullup bar')
    if user.resistanceBand:
        available_eqp.append('resistance band')
    if user.benchpressEquipment:
        available_eqp.append('bench')
    if user.medicineBall:
        available_eqp.append('medicine ball')

    return available_eqp


def find_exercise_pref(curr_user, exercise):
    # find exercise preference in the model
    return getattr(curr_user, exercise)

def find_exercise_diff(exercise):
    # find exercise difficulty in the model
    return 1


def get_valid_exercises(df, muscle, equipment_list):
    # returns list of valid exercises based on the target muscle and equipment list
    exercise_id_set = set()
    exercise_name_set = set()
    for eqp in equipment_list:
        for row in df.loc[(df['muscle'] == muscle) & (df[eqp])]['id'].unique():
            exercise_id_set.add(row)
        for row in df.loc[(df['muscle'] == muscle) & (df[eqp])]['exercise'].unique():
            exercise_name_set.add(row)

    return (list(exercise_set), list(exercise_name_set))


def fill_preferences(curr_user, exercises_list):
    # TODO: for current user
    # returns list of preference weight corresponding to the exercise list
    weight_list = []
    for exercise in exercises_list:
        weight_list.append(find_exercise_pref(curr_user, exercise))
    return weight_list


def fill_difficulty(health_score, exercises_list):
    # TODO: for current user
    # returns list of difficulty weight corresponding to the exercise list
    weight_list = []
    for exercise in exercises_list:
        weight_list.append(health_score * find_exercise_diff(exercise))
    return weight_list


def make_exercise_rec(df, muscle_list, equipment_list, curr_user):
    # returns list of exercises that we recommend the user based off their preferences
    final_recs = set()
    for muscle in muscle_list:
        exercises = get_valid_exercises(df, muscle, equipment_list)
        print(muscle, exercises)
        prefs = fill_preferences(curr_user, exercises)
        choices = random.choices(population=exercises, weights=prefs, k=50)

        counter = 0
        i = 0
        while i < len(choices) and counter < 2:
            if choices[i] not in final_recs:
                final_recs.add(choices[i])
                counter += 1
            i += 1
    return list(final_recs)


def get_sets_reps(df, final_exercises, overall_diff):
    # returns dict of {id: {sets, reps}} based off the overall difficulty for
    # each exercise
    out = {}
    print(df.loc[(df['id'] == 1)]['overallMax'])

    for i in range(len(final_exercises)):
        for index, row in df.loc[(df['id'] == final_exercises[i]) & (df['overallMin'] < overall_diff) & (
                    overall_diff < df['overallMax'])].iterrows():
            out[final_exercises[i]] = {}
            out[final_exercises[i]]['sets'] = row['sets']
            out[final_exercises[i]]['reps'] = row['reps']
    return out

def make_recommendations(curr_user):
    # returns dict of exercies with sets and reps
    # TODO: consider user and day of week
    # need this for when running from python3 manage.py runserver
    input_path = './app/exercises.csv'
    # otherwise working directory is app
    # input_path = '../app/exercises.csv'

    df = pd.read_csv(input_path)
    print(df)

    # get todays day of week, monday is 0 sunday is 6
    weekday = datetime.datetime.today().weekday()

    final_exercises = make_exercise_rec(df, ['calf', 'hamstring'], ["bodyweight", "barbell"], curr_user)
    print(final_exercises)
    overall_diff = find_exercise_diff(final_exercises)
    print(get_sets_reps(df, final_exercises, overall_diff))


    print(final_exercises)
"""
    valid_equipment = get_valid_equipment(curr_user)
    # if users goal is lose weight, less exercise days
    # recommend legs, core mon
    # recommend arms, back fri
    if curr_user.goal == 'L':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'calf', 'hamstring', 'core'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            pass
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep', 'back'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            pass


    # if users goal is gain muscle, more exercise days
    # recommend quads, hamstring mon
    # recommend bicep, tricep wed
    # recommend calf, core fri
    # recommend back sun
    elif curr_user.goal == 'G':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'hamstring'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep'], valid_equipment)
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['calf', 'core'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            final_exercises = make_exercise_rec(df, ['back'], valid_equipment)



    # if users goal is general, 3 exercise days
    # recommend quads, calf, hamstring mon
    # recommend bicep, tricep  wed
    # recommend core, back sat
    elif curr_user.goal == 'F':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'calf', 'hamstring'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep'], valid_equipment)
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['back', 'core'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            pass


Monday:    prev = None, so day 1: quad calf
Wednesday: prev = quad calf , so day 2: bicep tricep
Friday:    prev = bicep tricep, so day 3: back core
Monday:    prev = back core, so day 4: hamstring
Wednesday: prev = hamstring, so day 5: quad calf

    else:
        #invalid goal
        pass


# make_recommendations(1)
"""