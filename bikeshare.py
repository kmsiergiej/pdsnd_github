import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv' }

DATETIME_LISTS = {
    'months': ['january', 'february', 'march', 'april', 'may', 'june'],
    'days': ['Monday', 
            'Tuesday', 
            'Wednesday', 
            'Thursday',  
            'Friday', 
            'Saturday',
            'Sunday']
}

def get_months_input_msg():
    count = 1
    msg = 'Choose month by number: \n'
    for m in DATETIME_LISTS['months']:
        msg += '{} = {} \n'.format(count, m)
        count += 1
    msg += '0 = all \n'
    return msg

def get_days_input_msg():
    count = 1
    msg = 'Choose day by number: \n'
    for d in DATETIME_LISTS['days']:
        msg += '{} = {} \n'.format(count, d)
        count += 1
    msg += '0 = all \n'
    return msg

def get_input_error_msg(param, input_range):
    return 'Invalid param! You can only use one of the following params for {}: {}'.format(param, [i for i in input_range])

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Expect integer values as input from the user.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        cities = ['chicago', 'new york city', 'washington']
        try: 
            city_inp = int(input('\nChoose city: 1=Chicago, 2=New York City, 3=Washington.\n'))
            # check input data for city - only 1,2,3 are allowed
            r = range(1,4)
            if ( city_inp not in r):
                raise Exception(get_input_error_msg('city', r))
            
            month_inp = int(input(get_months_input_msg()))
            # check input data for monty - only numbers from 0 to 6 are allowed 
            r = range(0,7)
            if ( month_inp not in r):
                raise Exception(get_input_error_msg('month', r))

            day_inp = int(input(get_days_input_msg()))
            r = range(0,8)
            if ( day_inp not in r):
                raise Exception(get_input_error_msg('day', r))

            city = cities[city_inp-1]
            if month_inp == 0:
                month = 'all'
            else:
                month = DATETIME_LISTS['months'][month_inp-1]
            if day_inp == 0:
                day = 'all'
            else:
                day = DATETIME_LISTS['days'][day_inp-1]

            print('Calculating for following user input: ', city, month, day)
            break
        except Exception as ve:
            print('Error: {}. Try again!'.format(str(ve)))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = DATETIME_LISTS.get('months')
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_upper = day.title()
        days = DATETIME_LISTS.get('days')
        if day_upper not in days:
            msg = '''Day: {} is not available
            Please use on of the correct day names {}'''
            raise ValueError(msg.format(day_upper, days))
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = DATETIME_LISTS.get('months')
    days = DATETIME_LISTS.get('days')
    
    # display the most common month
    most_common_month = df['month'].value_counts().head(1).index.tolist()[0]
    print('The most common month is: {}'.format(months[most_common_month-1])) 

    # display the most common day of week
    most_common_week_day = df['day_of_week'].mode()[0]
    print('The most common day of week is: {}'.format(most_common_week_day))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is: {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    is_most_common_start_station = df['Start Station'] == most_common_start_station
    most_common_start_station_count = df[is_most_common_start_station]['Start Station'].value_counts()[0]

    print('The most common start station is: {}, Count: {}'.format(most_common_start_station, most_common_start_station_count))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    is_most_common_end_station = df['End Station'] == most_common_end_station
    most_common_end_station_count = df[is_most_common_end_station]['End Station'].value_counts()[0]

    print('The most common end station is: {}, Count: {}'.format(most_common_end_station, most_common_end_station_count))

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + ' - ' + df['End Station']
    most_common_combination = df['Start and End Station'].mode()[0]

    is_most_common_combination = df['Start and End Station'] == most_common_combination
    most_common_combination_count = df[is_most_common_combination]['Start and End Station'].value_counts()[0]

    print('The most common combination of start and end stations is: {}, Count: {}'.format(most_common_combination, most_common_combination_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_seconds = df['Trip Duration'].sum()

    s = int(total_travel_time_seconds)
    time_delta = datetime.timedelta(seconds=s)
    print('Total travel time: {}'.format(time_delta))

    # display mean travel time
    mean_travel_time_seconds = df['Trip Duration'].mean()
    s = int(mean_travel_time_seconds)

    time_delta = datetime.timedelta(seconds=s)
    print('Mean travel time: {}'.format(time_delta))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Counts of gender: \n', gender)

        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df['Birth Year'].min())
        print('Earliest year:', earliest_year)

        most_recent_year = int(df['Birth Year'].max())
        print('Most recent year:', most_recent_year)
    
        most_common_year = int(df['Birth Year'].mode()[0])
        print('Most common year:', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as ve:
        print('Error occured: {}. Try again!'.format(str(ve)))
