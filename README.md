# Indeed-Data-Scrape
Data gathering and analysis project using indeed.com 

Using pythons web scraping libraries, data will be gathered every day over an extended period of time.
The number of new jobs every day of different types and salaries is the data being gathered.

Linux's Crontab is being used to scedule the scrape for 23:50 every day on a raspberry pi
Data will be uploaded here every Monday.

Format of data in the csv is as follows:
  date, job type, +£0 jobs,  +£10k jobs, +£20k jobs, +£30k, +£40k, +£50k, +£60k
