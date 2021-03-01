from .models import Member
import datetime

curr_user = Member.objects.get(name="boby", age=10, "get current user somehow")


# returns list of exercies with sets and reps
def make_recommendations(curr_user):

    # get todays day of week, monday is 0 sunday is 6
    weekday = datetime.datetime.today().weekday()


    # if users goal is lose weight, less exercise days
    # recommend legs, core mon
    # recommend arms, back fri
    if curr_user.goal[0] == 'L':
        if weekday == 0:






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