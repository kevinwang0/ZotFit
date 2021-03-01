import pandas as pd
import xmltodict
import os


def a(username):
    print(os.getcwd())
    print(os.listdir())
    # need this for when running from python3 manage.py runserver
    # input_path = '/uploaded_files/apple_health_export_' + username + '/export.xml'
    # pickle_path = '/uploaded_files/apple_health_export_' + username + '/pickle_data'
    # otherwise working directory is app
    # need a way of story different files as different names, perhaps by username or id number
    input_path = '../uploaded_files/apple_health_export_' + username + '/export.xml'
    pickle_path = '../uploaded_files/apple_health_export_' + username + '/pickle_data'
    print(input_path)

    #pickling for now, only once
    """
    # i think pickling when we upload the file the first time is better, and then read_pickle to process dataframe
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
        step_counts = df[df['@type'] == 'HKQuantityTypeIdentifierStepCount']
        step_counts.loc[:, '@value'] = pd.to_numeric(
            step_counts.loc[:, '@value'])
        df[df['@type'] == 'HKQuantityTypeIdentifierStepCount'] = step_counts

        df.to_pickle(pickle_path)
    """
    df = pd.read_pickle(pickle_path)
    step_counts = df[df['@type'] == 'HKQuantityTypeIdentifierStepCount']

    # getting steps by day
    step_counts_by_creation = step_counts.groupby('@creationDate').sum()
    steps_by_day = step_counts_by_creation['@value'].resample('D').sum()
    print(steps_by_day)
    #print top 10 days
    print(steps_by_day.sort_values(ascending=False)[:10])

    # getting heart rate by day
    heart_rate = df[df['@type'] == 'HKQuantityTypeIdentifierHeartRate']

    heart_rate.loc[:, '@value'] = pd.to_numeric(
        heart_rate.loc[:, '@value'])

    heart_rate_by_creation = heart_rate.groupby('@creationDate').mean()
    heart_rate_day_avg = heart_rate_by_creation['@value'].resample('D').mean()
    print(heart_rate_by_creation)
    print(heart_rate_day_avg)

    """
    # getting rest heart rate by day
    rest_heart_rate = df[df['@type'] == 'HKQuantityTypeIdentifierRestingHeartRate']
    step_counts_by_creation = step_counts.groupby('@creationDate').sum()
    steps_by_day = step_counts_by_creation['@value'].resample('D').sum()
    print(steps_by_day)

    # getting walking heart rate by day
    walking_heart_rate = df[df['@type'] == 'HKQuantityTypeIdentifierWalkingHeartRateAverage']
    step_counts_by_creation = step_counts.groupby('@creationDate').sum()
    steps_by_day = step_counts_by_creation['@value'].resample('D').sum()
    print(steps_by_day)
    """





    print()
    print(df['@type'].unique())

a('brian_he')