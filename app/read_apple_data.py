import pandas as pd
import xmltodict
import os
import datetime
import pytz
from .models import MemberManager, Member, Workout
from django.contrib.auth.models import User

class StepData:
    def __init__(self, request):
        self.request = request
        if request.user.is_authenticated:
            self.user = Member.objects.get(user=request.user.id)
            print("AUTHENTICATED")
        else:
            print("UNAUTHENTICATED")
        self.recent_steps = []

    def get_recent_steps(self, num):
        self.recent_steps = []
        # get the steps that happened on the workoutDate
        print(Workout.objects.filter(user=self.request.user).filter(workoutName='steps').order_by('-workoutDate'))
        for workout in Workout.objects.filter(user=self.request.user).filter(workoutName='steps').order_by('-workoutDate'):
            print(workout.workoutDate, workout.steps)
            if len(self.recent_steps) > num:
                break
            self.recent_steps.append(workout.steps)
        # reverse recent_steps to get the correct ordering
        self.recent_steps = reversed(self.recent_steps)

    def save_step_data(self):
        
        # input_path = '../uploaded_files/apple_health_export_brian_he/export.xml'
        input_path = './uploaded_files/apple_health_export_brian_he/export.xml'
        # input_path = '/uploaded_files/apple_health_export_' + username + '/export.xml'
        with open(input_path, 'r') as xml_file:
            # converting xml to pandas dataframe
            input_data = xmltodict.parse(xml_file.read())
            records_list = input_data['HealthData']['Record']
            df = pd.DataFrame(records_list)
            print(df.columns)

            # converting to pandas datetime object
            format = '%Y-%m-%d %H:%M:%S %z'
            df['@creationDate'] = pd.to_datetime(df['@creationDate'],
                                                format=format)
            df['@startDate'] = pd.to_datetime(df['@startDate'],
                                            format=format)
            df['@endDate'] = pd.to_datetime(df['@endDate'],
                                            format=format)

            # converting steps to integer
            # dt = datetime.datetime(2020, 12, 12, 5,5,5,5)
            dt = self.user.latestUploadDate
            print(dt)
            dt = datetime.datetime(dt.year, dt.month, dt.day)
            dt = pytz.utc.localize(dt)
            step_counts = df.loc[(df['@type'] == 'HKQuantityTypeIdentifierStepCount') & (df['@creationDate'] > dt)]
            step_counts.loc[:, '@value'] = pd.to_numeric(step_counts.loc[:, '@value'])
            df[df['@type'] == 'HKQuantityTypeIdentifierStepCount'] = step_counts
    
            # getting steps by day
            step_counts_by_creation = step_counts.groupby('@creationDate').sum()
            steps_by_day = step_counts_by_creation['@value'].resample('D').sum()


            # dt2 = dt = datetime.datetime(2021, 1, 1, 5,5,5,5)
            # dt_aware2 = pytz.utc.localize(dt)
            # for index, row in steps_by_day.items():
            #     print("Date: ", index, "Steps", row)
            # print(steps_by_day[steps_by_day.index > dt_aware2])

            # get the rows where the creation date is greater than the latest upload date
            # for each of those, get the index (date) and the value (steps) and store them in a workout object
            # put the list of workout objects in the database

            iterrows = steps_by_day.items()
            save_to_db = [
                Workout(user = self.request.user,
                        workoutName = "steps",
                        workoutDate = index.date(),
                        steps = value)
                for index, value in iterrows
            ]
            self.user.latestUploadDate = datetime.date.today()
            Workout.objects.bulk_create(save_to_db)
            self.user.save()
            
            # steps_by_day.loc[steps_by_day[]]

# s = StepData()
# s.save_step_data()




# """
# def a(username):
#     print(os.getcwd())
#     print(os.listdir())
#     # need this for when running from python3 manage.py runserver
#     # input_path = '/uploaded_files/apple_health_export_' + username + '/export.xml'
#     # pickle_path = '/uploaded_files/apple_health_export_' + username + '/pickle_data'
#     # otherwise working directory is app
#     # need a way of story different files as different names, perhaps by username or id number
#     input_path = '../uploaded_files/apple_health_export_' + username + '/export.xml'
#     pickle_path = '../uploaded_files/apple_health_export_' + username + '/pickle_data'
#     print(input_path)

#     #pickling for now, only once
#     """
#     """
#     # i think pickling when we upload the file the first time is better, and then read_pickle to process dataframe
#     with open(input_path, 'r') as xml_file:
#         # converting xml to pandas dataframe
#         input_data = xmltodict.parse(xml_file.read())
#         records_list = input_data['HealthData']['Record']
#         df = pd.DataFrame(records_list)
#         print(df.columns)

#         # converting to pandas datetime object
#         format = '%Y-%m-%d %H:%M:%S %z'
#         df['@creationDate'] = pd.to_datetime(df['@creationDate'],
#                                              format=format)
#         df['@startDate'] = pd.to_datetime(df['@startDate'],
#                                           format=format)
#         df['@endDate'] = pd.to_datetime(df['@endDate'],
#                                         format=format)

#         # converting steps to integer
#         step_counts = df[df['@type'] == 'HKQuantityTypeIdentifierStepCount']
#         step_counts.loc[:, '@value'] = pd.to_numeric(
#             step_counts.loc[:, '@value'])
#         df[df['@type'] == 'HKQuantityTypeIdentifierStepCount'] = step_counts

#         df.to_pickle(pickle_path)
#     """
#     """
#     df = pd.read_pickle(pickle_path)
#     step_counts = df[df['@type'] == 'HKQuantityTypeIdentifierStepCount']

#     # getting steps by day
#     step_counts_by_creation = step_counts.groupby('@creationDate').sum()
#     steps_by_day = step_counts_by_creation['@value'].resample('D').sum()
#     print(steps_by_day)
#     #print top 10 days
#     print(steps_by_day.sort_values(ascending=False)[:10])

#     # getting heart rate by day
#     heart_rate = df[df['@type'] == 'HKQuantityTypeIdentifierHeartRate']

#     heart_rate.loc[:, '@value'] = pd.to_numeric(
#         heart_rate.loc[:, '@value'])

#     heart_rate_by_creation = heart_rate.groupby('@creationDate').mean()
#     heart_rate_day_avg = heart_rate_by_creation['@value'].resample('D').mean()
#     print(heart_rate_by_creation)
#     print(heart_rate_day_avg)

#     print()
#     print(df['@type'].unique())

# a('brian_he')
# """