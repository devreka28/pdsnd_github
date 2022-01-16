import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Docstring will be added to all functions. They can be printed by using print(<function name>.__doc__)
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
# checks if correct input has been given for city
    while True:
        city_input=input("Please choose which city you would like to see: Chicago New York or Washington? ")

        try:
            if city_input in ['chicago','Chicago','New York','new york','new york city','New York City','Washington','washington']:
                break
            else:
                print("Sorry, your input should be chicago, new york city or washington.")

        except ValueError:
            print("Sorry, your input is wrong. Try again using one of the cities' name.")

# converts city to lower case to that it can be used as filter
    city=city_input.lower()
# checks if correct input has been given for month
    while True:
        month_input=input("Please choose which month you would like to analyse: January, February, March, April, May or June? Type 'None' for no month filter. ")
        try:
            if month_input in['january','January','february','February', 'march', 'March', 'april', 'April', 'may', 'May', 'june', 'June', 'None']:
                break
            else:
                print("This is not a valid month name or 'None'. Please try again.")
        except ValueError:
            print("Sorry, your input is wrong. Try again using one of the months' name or 'None'.")

# converts month name to lower case to that it can be used as filter but keeps None as it is else an empty df will be returned when this is selected
    if month_input!='None':
        month=month_input.lower()
    else:
        month=month_input


    while True:
        day_input=input ("Please choose which day you would like to analyse: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday. Type 'None' for no day filter. ")
        try:
            if day_input in ['monday','Monday','tuesday','Tuesday','wednesday','Wednesday','thursday','Thursday','friday','Friday','saturday','Saturday','sunday','Sunday','None']:
                break
            else:
                print("This is not a valid day name or 'None'. Please try again.")
        except ValueError:
            print("Sorry, your input is wrong. Try again using one of the months' name or 'None'.")

# converts month name to lower case to that it can be used as filter but keeps None as it is else an empty df will be returned when this is selected

    if day_input!= 'None':
        day=day_input.lower()
    else:
        day=day_input
    return (city, month, day)


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

    # loads data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracts month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filters by month if applicable
    if month != 'None':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filters by month to create the new dataframe
        df = df[df['month'] == month]

    # filters by day of week if applicable
    if day != 'None':
        # filters by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    print(df)

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Uses value_counts method to find the most popular month
    popular_month = df['month'].value_counts().idxmax()

    print("The most popular month is (1 = January,...,6 = June): {}".format(popular_month))


    #Uses value_counts method to find the most popular day
    popular_day = df['day_of_week'].value_counts().idxmax()

    print("\nMost Popular Day: {}".format(popular_day))

    #Extracts hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Uses value_counts method to find the most popular hour
    popular_hour = df['hour'].value_counts().idxmax()

    print("\nMost Popular Start Hour: {}".format(popular_hour))

    # display the most common start hour

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics about the most popular stations, trips and combination of trips."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #Uses value_counts method to find the most popular station
    common_start_station = df['Start Station'].value_counts().idxmax()
    # displays the most commonly used start station
    print("The most commonly used start station: {}".format(common_start_station))

    #Uses value_counts method to find the most popular station
    common_end_station = df['End Station'].value_counts().idxmax()
    # displays the most commonly used end station
    print("\nThe most commonly used end station: {}".format(common_end_station))

    #Uses str.cat to combine two columsn in the dataframe then the value_counts() method counts these
    #unique values to see which trip was the most popular

    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combination = df['Start To End'].value_counts().idxmax()
    # display most frequent combination of start station and end station trip
    print("\nThe most frequent combination of trips are from {}".format(combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_duration = df['Trip Duration'].sum()
    # converts the seconds to minutes and hours
    hour = total_duration // 3600
    minute= round((total_duration % 3600)/60)
    # displays the total duration in second and rounded hour and minutes format
    print('The total travel time is {} in seconds which is {} hours and {} minutes'.format(total_duration,hour,minute))
    #Calculating the average trip duration using mean method
    average_duration = df['Trip Duration'].mean()
    # converts seconds to hours and minutes format
    a_minute = round(average_duration // 60)
    a_second = round(average_duration % 60)
    # displays the total duration in second and rounded minutes and seconds format
    print('\nThe average travel time is {} in seconds which is {} minutes and {} seconds'.format(average_duration,a_minute,a_second))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users where available.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #The values in 'User Type' are counted by the value_counts method.

    user_type = df['User Type'].value_counts()

    print("The number of different user types:\n{}".format(user_type))

    # Try clauses to handle Washington data which does not have gender and birth year data
    try:
        gender = df['Gender'].value_counts()
        print("\nThe types of users by gender are given below:\n\n{}".format(gender))
    except:
        print("\nThere is no 'Gender' column in this file.")


    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].value_counts().idxmax())
        print("\nThe earliest year of birth is: {}\n\nThe most recent year of birth is: {}\n\nThe most common year of birth: {}".format(earliest,recent,common_year))
    except:
        print("There are no birth year details in this file.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)


def display_data(df):
    ''' Displays raw data: five rows at a time until the user selects no. '''
# while loop to check if valid input is given when requested for the first times
# if 'yes' is the input, using iloc the first 5 rows are selected and all nine columns
    while True:
        response=['yes','no']
        choose_response = input("Would you like to view the next five individual trip data entries? Type exactly 'yes' or 'no'\n").lower()
        if choose_response in response:
            if choose_response=='yes':
                start=0
                end=5
                data = df.iloc[start:end,:9]
                print(data)
            break
        else:
            print("This is not a valid response. Please try again.")
# if clause for when 'yes' input is made not for the first time
# the start and end variables always increase by 5 so that each time it displays the
# following five rows of the dataframe
    if  choose_response=='yes':
            while True:
                choose_response_2= input("Would you like to view more trip data? Type 'yes' or 'no'\n").lower()
                if choose_response_2 in response:
                    if choose_response_2=='yes':
                        start+=5
                        end+=5
                        raw_data = df.iloc[start:end,:9]
                        print(raw_data)
                    else:
                        break
                else:
                    print("This is not a valid response, please try again.")


def main():
    """The main fuction which calls all the other functions"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
