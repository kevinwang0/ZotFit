#from .models import Member
import datetime
import pandas as pd
import random

# curr_user = Member.objects.get(name="boby", age=10, "get current user somehow")

def get_valid_equipment(user):
    available_eqp = ['bodyweight']
    if user.barbell:
        available_eqp.append('barbell')
    if user.dumbbell:
        available_eqp.append('dumbbell')
    if user.pullup_bar:
        available_eqp.append('pullup bar')
    if user.resistance_band:
        available_eqp.append('resistance band')
    if user.bench:
        available_eqp.append('bench')
    if user.medicine_ball:
        available_eqp.append('medicine ball')

    return available_eqp


def find_exercise_pref(exercise):
    # find exercise preference in the model
    return 1

def find_exercise_diff(exercise):
    # find exercise difficulty in the model
    return 1


def get_valid_exercises(df, muscle, equipment_list):
    exercise_set = set()
    for eqp in equipment_list:
        for row in df.loc[(df['muscle'] == muscle) & (df[eqp])]['id'].unique():
            exercise_set.add(row)
    return list(exercise_set)


def fill_preferences(exercises_list):
    weight_list = []
    for exercise in exercises_list:
        weight_list.append(find_exercise_pref(exercise))
    return weight_list


def fill_difficulty(health_score, exercises_list):
    weight_list = []
    for exercise in exercises_list:
        weight_list.append(health_score * find_exercise_diff(exercise))
    return weight_list

def make_exercise_rec(df, muscle_list, equipment_list):
    final_recs = set()
    for muscle in muscle_list:
        exercises = get_valid_exercises(df, muscle, equipment_list)
        print(muscle, exercises)
        prefs = fill_preferences(exercises)
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
    out = []
    print(df.loc[(df['id'] == 1)]['overallMax'])
    df2 = pd.DataFrame(columns = (df.columns))

    for i in range(len(final_exercises)):
        df2.append(df.loc[(df['id'] == final_exercises[i]) & (df['overallMin'] < overall_diff) & (
                    overall_diff < df['overallMax'])], ignore_index = True)
    print(df2)
    without_repeats = set()
    exercises = []


# returns list of exercies with sets and reps
def make_recommendations(curr_user):
    # need this for when running from python3 manage.py runserver
    # input_path = '/app/exercises.csv'
    # otherwise working directory is app
    input_path = '../app/exercises.csv'

    df = pd.read_csv(input_path)
    print(df)

    # get todays day of week, monday is 0 sunday is 6
    weekday = datetime.datetime.today().weekday()

    final_exercises = make_exercise_rec(df, ['calf', 'hamstring'], ["bodyweight", "barbell"])
    print(final_exercises)
    overall_diff = find_exercise_diff(final_exercises)
    get_sets_reps(df, final_exercises, overall_diff)


    print(final_exercises)
    """
    valid_equipment = get_valid_equipment(curr_user)
    # if users goal is lose weight, less exercise days
    # recommend legs, core mon
    # recommend arms, back fri
    if curr_user.goal[0] == 'L':
        if weekday == 0:
            final_exercises = make_exercise_rec(df, ['quadricep', 'calf', 'hamstring', 'core'], valid_equipment)
        elif weekday == 1:
            pass
        elif weekday == 2:
            pass
        elif weekday == 3:
            pass
        elif weekday == 4:
            final_exercises = make_exercise_rec(df, ['bicep', 'tricep, 'back'], valid_equipment)
        elif weekday == 5:
            pass
        elif weekday == 6:
            pass








    # if users goal is gain muscle, more exercise days
    # recommend quads, hamstring mon
    # recommend bicep, tricep wed
    # recommend calf, core fri
    # recommend back sun
    elif curr_user.goal[0] == 'G':
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
    elif curr_user.goal[0] == 'F':
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

    else:
        #invalid goal
    """

make_recommendations(1)