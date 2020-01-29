import sys
import csv
import pandas as pd
from datetime import date, timedelta, datetime
import seaborn as sns
import matplotlib.pyplot as plt

###
def prepareData():
    columnTitles = ["date", "type", "total", "0-9.999k", "10-19.999k", "20-29.999k", "30-39.999k"
                        , "40-49.999k", "50-59.999k", "60k+"]

    jobsData = pd.read_csv('jobsData.csv').T.reset_index().T.reset_index(drop=True)
    jobsData.columns = columnTitles

    for title in columnTitles[2:13]:
        jobsData[title] = pd.to_numeric(jobsData[title])

    return jobsData

###
def getDateRange():
    ##
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    startDate = datetime.strptime(jobsData.iloc[0,0] , '%Y-%m-%d').date()
    endDate = datetime.strptime(jobsData.iloc[-1,0] , '%Y-%m-%d').date()

    dateRange = []
    for single_date in daterange(startDate, endDate):
        dateRange.append(single_date.strftime("%Y-%m-%d"))

    return dateRange

###
def calcDailyAverages():
    columnTitles = ["total", "0-9.999k", "10-19.999k", "20-29.999k", "30-39.999k"
                    , "40-49.999k", "50-59.999k", "60k+"]

    allAveragesData = []

    for jobType in jobsData.type.unique():
        dataByType = jobsData[jobsData['type'] == jobType]
        
        jobTypeAverages = {}
        jobTypeAverages["type"] = jobType
        for salaryRange in columnTitles:
            averageBySalary = int(dataByType[salaryRange].sum() / daysOfData)
            jobTypeAverages[salaryRange] = averageBySalary

        allAveragesData.append(jobTypeAverages)
    
    averagesDataFrame = pd.DataFrame(allAveragesData)
    
    return averagesDataFrame
    

###
def plotNewJobsByDay():
    sns.set_style("whitegrid")
    sns.set(rc={'figure.figsize':(15,7)})

    fig1 = sns.barplot(x='date', y='total',hue='type' , data=jobsData)
    fig1.set(xlabel = "Date", ylabel = "Number of New Jobs")
    plt.show(fig1)


###
def plotDailyAverages():
    sns.set_style("whitegrid")

    f, axes = plt.subplots(2, 4, figsize=(7, 7))

    sns.barplot(x='total', y='type' , data=dailyAveragesDataFrame, ax=axes[0, 0])
    sns.barplot(x='0-9.999k', y='type' , data=dailyAveragesDataFrame, ax=axes[0, 1])
    sns.barplot(x='10-19.999k', y='type' , data=dailyAveragesDataFrame, ax=axes[0, 2])
    sns.barplot(x='20-29.999k', y='type' , data=dailyAveragesDataFrame, ax=axes[0, 3])

    sns.barplot(x='30-39.999k', y='type' , data=dailyAveragesDataFrame, ax=axes[1, 0])
    sns.barplot(x='40-49.999k', y='type' , data=dailyAveragesDataFrame, ax=axes[1, 1])
    sns.barplot(x='50-59.999k', y='type' , data=dailyAveragesDataFrame, ax=axes[1, 2])
    sns.barplot(x='60k+', y='type' , data=dailyAveragesDataFrame, ax=axes[1, 3])
    plt.show(axes.all())


###
if __name__ == '__main__':

    jobsData = prepareData()
    dateRange = getDateRange()
    daysOfData = len(dateRange)
    dailyAveragesDataFrame = calcDailyAverages()

    plotNewJobsByDay()
    plotDailyAverages()
