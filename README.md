# Indeed-Data-Scrape
Data gathering and analysis project using indeed.com 

Using pythons web scraping libraries, data will be gathered every day over an extended period of time.
The number of new jobs every day of different types and salary ranges is the data being gathered.

Linux's Crontab was used to scedule the scrape for 23:50 every day on a raspberry pi.

Data was collected from the 28th Jan 2020 to the 5th of April 2020

Format of data in the csv is as follows:
  date, job type, £1-9.999k,  £10k-19.999k, £20k-29.999k, £30k-39.999k, £40k-49.999k, £50k-59.999k, £60k+
