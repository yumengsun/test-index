'''
@author: Yumeng Sun

'''
import sqlite3
import os
import pandas as pd
import re
import datetime
import numpy as np
import collections

# Global Variables
numDaysBack = 30
nTop = 50



#read in data from the 10M-line data from csv file
def readInData():
    path = os.path.join(os.getcwd(), "input.csv")
    df = pd.read_csv(path)
    return df
#return a set of all the dates from the original table
def getDateSet(df):
    return list(set(df['date']))
#use regular exspressions to extract all the domain names 
#return a new table with two columns: entry date and domain name
def getNewDF(df):    
    domain = []
    for s in df['emailAddress']:
        domain.append(re.search("@[\w.]+", s).group())
    domain_set = list(set(domain))
    new_df = np.transpose(np.array([df['date'],domain]))
    return new_df
#return a dictionary of domain-count pairs for any given date
def getDomCount(date, new_df):
    subset = new_df[new_df[:,0] == date]
    return dict(collections.Counter(subset[:,1]))



#Task 1: update another table which holds a daily count of email addresses by their domain name
def updateTable(dates,newdf):
    conn = sqlite3.connect('test.db')
    print(datetime.datetime.now().strftime("%H:%M:%S") + "\tBEGIN : Updating DailyCount table in test.db")
    #create table
    conn.execute("DROP TABLE IF EXISTS DailyCount;")
    conn.execute('''CREATE TABLE DailyCount
       (domain           TEXT    NOT NULL,
       count            INT     NOT NULL,
       entryDate         DATE NOT NULL);''')
    #insertion: domain, count and entryDate
    l = []
    for date in dates:
        dic = getDomCount(date, newdf)
        for k, v in dic.items():
            l.append((k,v,date))
    query = "INSERT INTO DailyCount (domain, count, entryDate) VALUES (?, ?, ?)"
    conn.executemany(query, l)
    #commit
    conn.commit()
    conn.close()
    print(datetime.datetime.now().strftime("%H:%M:%S") + "\tFINISH : Updated DailyCount table in test.db")



#Task2: Use the new table to report the top 50 domains by count sorted by percentage growth of the last 30 days compared to the total.
def generateReport(minDate):
    print(datetime.datetime.now().strftime("%H:%M:%S") + "\tBEGIN : Generating Report")
    conn = sqlite3.connect('test.db')
    #get total counts for each domain name
    cursor_total = conn.execute("SELECT domain, sum(count) FROM DailyCount GROUP BY domain")
    #save the domain-count pairs as a dictionary
    totalDict = {}
    for item in cursor_total.fetchall():
        totalDict[str(item[0])] = item[1]
    #minDate: the date which is 30 days before the most recent date in the table
    #get total counts during the past 30 days for each domain 
    cursor_past = conn.execute("SELECT domain, sum(count) FROM DailyCount WHERE entryDate > ? GROUP BY domain", 
                           [minDate.date()])
    #save the domain-count pairs as a dictionary
    inc = {}
    for item in cursor_past.fetchall():
        inc[str(item[0])] = item[1]
    conn.close()
    #get the percentage by increase/total
    incPercent = {k: float(inc[k])/totalDict[k] for k in totalDict.viewkeys() & inc.viewkeys()}
    repDom = []
    repPerc = []
    #skip those domains who have no records before minDate(the date which is 30 days before the most recent date in the table).
    #get top 50 and write into csv file 'report.csv'
    i=1
    for w in sorted(incPercent, key=incPercent.get,reverse=True):
        if(incPercent[w]<1):
            repDom.append(w)
            repPerc.append(incPercent[w])
            i = i+1
        if(i>nTop):
            break
    f = open('report.csv', 'w')
    f.write("rank,domain,percent\n")
    for i in range(nTop):
        f.write("%d,%s,%f\n" % (i+1, repDom[i], repPerc[i]))
    f.close()   
    print(datetime.datetime.now().strftime("%H:%M:%S") + "\tFINISH : Report generated. Please refer to file 'report.csv'.")


def main():
    print(datetime.datetime.now().strftime("%H:%M:%S") + "\nThis script takes around 2 minutes to run on my 3 year old Macbook Air.\n The test dataset contains 10,000,000 email addresses with 100,000 domains.\n The entry dates range from 2015-08-01 to 2015-09-30.\n")
    print(datetime.datetime.now().strftime("%H:%M:%S") + "\tBEGIN : Data pre-processing")
    df = readInData()
    dates = getDateSet(df)
    newdf = getNewDF(df)
    print(datetime.datetime.now().strftime("%H:%M:%S") + "\tFINISH : Data pre-processed")
    updateTable(dates,newdf)
    maxDate = datetime.datetime.strptime(max(dates),"%Y-%m-%d")
    minDate = maxDate - datetime.timedelta(numDaysBack)
    generateReport(minDate)


if __name__ == "__main__":
    main()
