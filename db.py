import pymongo
import os
from pymongo import MongoClient

cluster = MongoClient('<Database>')
dbAll = cluster["money"]
dbx = dbAll["dbx"] #Select preset database collection
dbc = dbAll["dbc"] #Select preset database collection
db = [dbx,dbc]
monthtype = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "All"]
category = ["Budget","Food", "Transport", "Bills", "Shopping", "Fun", "Gifts", "Others"]

#Update document item
def update(year, month, type, value, db_type):
    dbtype = db[db_type]
    old = find(year, month, db_type)
    old_value = old[type]
    if type == 0:
        old[type] = value
    else:
        old[type] += value
    data = {"$set": {monthtype[month]: old}}
    query = {"_id": year}
    dbtype.update_one(query, data)
    return [type, old_value, old[type]]

#Find document and field
def find(year, month, db_type):
    dbtype = db[db_type]
    data = dbtype.find({"_id": year}, {"_id": 0, monthtype[month]: 1})
    return data[0][monthtype[month]]

#Create new month field
def create_new_month(year, month, db_type):
    dbtype = db[db_type]
    data = {"$set": {monthtype[month]: [0,0,0,0,0,0,0,0]}}
    query = {"_id": year}
    dbtype.update_one(query, data)

#Create new year document 
def create_new_year(year, db_type):
    dbtype = db[db_type]
    data = {"_id": year, "All": [0,0,0,0,0,0,0,0]}
    dbtype.insert_one(data)

#Reset year document
def reset_year(year, db_type):
    dbtype = db[db_type]
    dbtype.delete_one({"_id": year})
    create_new_year(year, db_type)

#Reset month field
def reset_month(year, month, db_type):
    dbtype = db[db_type]
    old = find(year, month, db_type)
    all = find(year, 12, db_type)
    for x in range(8):
        all[x] -= old[x]
    data = {"$set": {monthtype[12]: all}}
    query = {"_id": year}
    dbtype.update_one(query, data)
    create_new_month(year, month, db_type)

#Reset entire collection
def reset_collection(db_type):
    dbtype = db[db_type]
    dbtype.delete_many({})

#Checks if document and field exists
def check_data(year, month, type, db_type):
    dbtype = db[db_type]
    try:
        if type == 0:
            dbtype.find({"_id": year}, {"_id": 1})[0]
        else:
            find(year, month, db_type)
        return True
    except:
        return False

#Counts number of month field in year document
def count_months(year, db_type):
    dbtype = db[db_type]
    data = dbtype.find({"_id": year}, {"_id": 0})
    return len(data[0])
