import sys
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import time
import csv

###
def newLine():
    print("\n")

###
def buildURLS(jobType):
    urlList = []

    print("Building URL's")
    newLine()
    typeURL = "https://www.indeed.co.uk/jobs?l=United+Kingdom&fromage=1&jt="  + jobType

    for salary in minSalaries:
        salaryAndTypeURL = typeURL + "&q=" + salary
        urlList.append(salaryAndTypeURL)

    return urlList

###
def getHTML(urlList):
    htmlList = []
    continueChecking = True
    requestsRetryCount = 0

    while continueChecking:
        print("Fetching HTML")
        for url in urlList:
            # Need to request all with minimal delay between requests
            # Long delay means more time for new jobs to be added on website
            # New jobs being added between html requests produces inconsistent data
            print("Requesting HTML from:  " + url)
            targetHTML = requests.get(url)
            htmlList.append(targetHTML)

        newLine()
        print("Checking requested html status...")
        for htmlRequest in htmlList:
            if htmlRequest.status_code == 200:
                print("No HTML request Errors")
                continueChecking = False
            else:
                print("HTML request returned error status code: " + str(htmlRequest.status_code))
                if requestsRetryCount > 5:
                    print("Failed to fetch target HTML")
                    print("Unknown number of Jobs Matching criteria!")
                    htmlList = [None] * len(htmlList)
                    continueChecking = False
                    break
                else:
                    time.sleep(2)
                    print("Retrying...")
                    requestsRetryCount += 1
                    print("Retry attempt " + str(requestsRetryCount))
                    break

    return htmlList

###
def getSoup(htmlList):
    HTMLSoupList = []

    newLine()
    print("Screening fetched HTML...")
    if htmlList[0] != None:
        for targetHTML in htmlList:
            soup = BeautifulSoup(targetHTML.text, 'html.parser')
            targetHTMLSoup = soup.select('#searchCountPages')
            if len(targetHTMLSoup) > 0:
                print("New job data found.")
                HTMLSoupList.append(targetHTMLSoup)
            else:
                print("No new job data matching criteria.")
                HTMLSoupList.append("NO NEW JOBS")
    else:
        print("Skipping Null Data")
        HTMLSoupList = [None] * len(htmlList)

    return HTMLSoupList

###
def scrapeNewJobData(jobTypesToScrape):

    typesToRescrape = []
    for type in jobTypesToScrape:
        newLine()
        print("Scraping for new " + type + " jobs")
        newLine()

        soupList = getSoup(getHTML(buildURLS(type)))

        newLine()
        print("Extracting Data...")

        rawJobsDataDict[type] = []
        lastJobCount = None

        for soup in soupList:
            if soup == None:
                print("Skipping Null Data")
                rawJobsDataDict[type] = [None] * len(soupList)
                break
            elif soup == "NO NEW JOBS":
                jobCount = 0
            else:
                jobCount = soup[0]
                # String will be in the format, 'Page 1 of 27 jobs'
                # The number before 'jobs' is the target date
                jobCount = jobCount.string.replace(" ","")[8:-4]
                # Target data may contain commas eg '8,000'
                jobCount = jobCount.replace(",", "")
                jobCount = int(jobCount)

                if lastJobCount == None:
                    lastJobCount = jobCount
                elif lastJobCount < jobCount:
                    print("Inconsistent data detected! Will retry " + type + " job scrape")
                    typesToRescrape.append(type)
                    rawJobsDataDict[type] = []
                    break

                lastJobCount = jobCount

            rawJobsDataDict[type].append(jobCount)
            print("Extraction Complete: " + str(jobCount))

    currentLoopBadDataCount = len(typesToRescrape)
    if currentLoopBadDataCount > 0:
        newLine()
        print("Retrying " + str(currentLoopBadDataCount) +  " inconsistent data scrapes")
        rescrapeCount = scrapeNewJobData(typesToRescrape) + currentLoopBadDataCount
        return rescrapeCount

    return 0

###
def initialDataProcessing(rawJobsDataDict):
    print("Performing initial data processing...")
    processedJobsDataDict = {}
    for type in allJobTypes:
        processedData = []
        rawData = rawJobsDataDict[type]
        rawData.reverse()

        if rawData[0] != None:

            processedData.append(rawData[0])
            for i in range(0, len(rawData)-1):
                processedData.append(rawData[i+1]-rawData[i])

            processedData.append(rawData[-1])
            processedData.reverse()
        else:
            processedData = [""] * len(rawData)
            
        processedJobsDataDict[type] = processedData
    
    return processedJobsDataDict


##### MAIN #####
if __name__ == '__main__':

    todaysDate = date.today()
    allJobTypes = ["fulltime", "permanent", "parttime", "temporary", "contract",
                "apprenticeship", "commission", "volunteer", "internship"]
    minSalaries = ["£0", "£10,000","£20,000","£30,000",
                    "£40,000","£50,000", "£60,000"]
    rawJobsDataDict = {}

    newLine()
    print("!!! Indeed.co.uk Daily Job Scrapper !!!")

    totalRescrapes = scrapeNewJobData(allJobTypes)
    newLine()
    print("Scrape Sucessfull!")
    print(str(totalRescrapes) + " Rescrapes were performed")

    processedJobsDataDict = initialDataProcessing(rawJobsDataDict)

    print("Writing results to file: jobs.csv")
    with open('jobsData.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for type in allJobTypes:
            writer.writerow([todaysDate] + [type] + processedJobsDataDict[type])
