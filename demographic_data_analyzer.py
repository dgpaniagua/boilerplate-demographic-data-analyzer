import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    df_race = df.groupby(['race']).size().reset_index()
    df_race = df_race.set_index('race')
    df_race = df_race.sort_values(by=0,ascending=False)
    race_count = df_race.squeeze()
    # What is the average age of men?
    average_age_men = round(df.loc[df['sex']=="Male"]["age"].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df.loc[df["education"]=="Bachelors"].size / df.size)*100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = round((df.loc[(df["education"]=="Bachelors") | (df["education"]=="Masters") | (df["education"]=="Doctorate")].size / df.size)*100, 1)
    lower_education = 100 - higher_education

    # percentage with salary >50K
    higher_education_df = df.loc[(df["education"]=="Bachelors") | (df["education"]=="Masters") | (df["education"]=="Doctorate")]

    higher_education_rich_df = df.loc[((df["education"]=="Bachelors") | (df["education"]=="Masters") | (df["education"]=="Doctorate")) & (df["salary"]==">50K")]
    higher_education_rich = round((higher_education_rich_df.size / higher_education_df.size)*100, 1)
    
    df_rich = df.loc[df["salary"]==">50K"]
    lower_education_rich = round(((df_rich.size - higher_education_rich_df.size) / (df.size - higher_education_df.size))*100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df.loc[(df["hours-per-week"]==min_work_hours)].size

    rich_percentage = round((df.loc[(df["hours-per-week"]==min_work_hours) & (df["salary"]==">50K")].size / num_min_workers)*100, 1)

    # What country has the highest percentage of people that earn >50K?
    dfgb_50k = df.groupby(['salary','native-country']).size()
    df_50k = dfgb_50k.reset_index()
    df_50k = df_50k.set_index('native-country')
    df_50k = df_50k.loc[df_50k['salary']=='>50K']
    dfgb_country = df.groupby(['native-country']).size()
    df_country=dfgb_country.reset_index()
    df_country=df_country.set_index('native-country')
    rate = df_country.join(df_50k, lsuffix='_caller',rsuffix='_other')
    rate['rate'] = (rate['0_other'] / rate['0_caller'])*100
        
    highest_earning_country = rate.loc[rate['rate'].max()==rate['rate']].index.item()
    highest_earning_country_percentage = round(rate['rate'].max(), 1)
    
    # Identify the most popular occupation for those who earn >50K in India.
    dfgb_india = df.loc[(df['salary']=='>50K') & (df['native-country']=='India')].groupby(['occupation']).size()
    df_india =dfgb_india.reset_index()
    top_IN_occupation = df_india['occupation'].loc[df_india[0].max()==df_india[0]].item()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }