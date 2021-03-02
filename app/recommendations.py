#from .models import Member
import datetime
import pandas as pd

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


def get_valid_exercises(df, muscle, list_of_equipment):
    exercise_set = set()
    for eqp in list_of_equipment:
        for row in df.loc[(df['muscle'] == muscle) & (df[eqp])]['id'].unique():
            exercise_set.add(row)
    print(exercise_set)
    return exercise_set
        # print(df.loc[(df['body part'] == muscle) & (df[eqp])])


def fill_preferences(exercises_list):
    [0 - 0.8, 0.8 - 1.8, 2 - 3, ..., 34 - 35]
    r = random()
    r = 0.2
    exercise = [1,3]

# returns list of exercies with sets and reps
def make_recommendations(curr_user):
    # need this for when running from python3 manage.py runserver
    # input_path = '/app/exercises.csv'
    # otherwise working directory is app
    input_path = '../app/exercises.csv'

    df = pd.read_csv(input_path)
    print(df)
    valid_calf_exercies = get_valid_exercises(df, "calf", ["bodyweight", "barbell"])

    # get todays day of week, monday is 0 sunday is 6
    weekday = datetime.datetime.today().weekday()



    """
    # if users goal is lose weight, less exercise days
    # recommend legs, core mon
    # recommend arms, back fri
    if curr_user.goal[0] == 'L':
        if weekday == 0:
            # get valid exercises depending on equipment
            # get exercise preferences
            # randomly pick exercises
            # get sets and reps from df






    # if users goal is gain muscle, more exercise days
    # recommend legs mon
    # recommend arms wed
    # recommend core fri
    # recommend back sun
    elif curr_user.goal[0] == 'G':





    # if users goal is general, 3 exercise days
    # recommend legs mon
    # recommend arms wed
    # recommend core, back sat
    elif curr_user.goal[0] == 'F':


    else:
        #invalid goal
    """


make_recommendations(1)