#-----------------Import Dependencies----------------------------# 
import xlrd
import csv
from glob2 import glob
import os
import pandas as pd
import json
import pymongo
from pymongo import MongoClient
from bson.binary import Binary
#----------------------------------------------------------------#
#Siva : 9/13/2018. Updated to create one database and use the mlab cloud mongodb.

def JSON_from_excel():
        filePath = ""
        xlsFilesOnly = glob(filePath+"*.xls")# parse all xls file(s) only
        StateList = []
        for xlsfile in xlsFilesOnly:
            # xlsfilename = xlsfile.split(" ") # get the year of the file
            # year = xlsfilename[0]
            yearReported = xlsfile[:4]
            wb = xlrd.open_workbook(xlsfile,ragged_rows = True)
            
            if (wb != None):    
                sh = wb.sheet_by_name('OutcomesFactorsSubRankings') 
                CountyList = []
                if (sh != None): 

                    for row_index in range(sh.nrows):
                        HealthyCounty = {}
                        if(row_index > 2 ):
                            
                            StateName = sh.cell(row_index, 1 ).value #---unused at the moment

                            QualityofLife = { 
                                "Z-Score" : sh.cell(row_index, 3 ).value,
                                "Rank" : sh.cell(row_index, 4 ).value,
                            }   

                            HealthBehaviours = {
                                "Z-Score" : sh.cell(row_index, 5 ).value,
                                "Rank" : sh.cell(row_index, 6 ).value,
                            }                         

                            ClinicalCare = {
                                "Z-Score" : sh.cell(row_index, 7 ).value,
                                "Rank" : sh.cell(row_index, 8 ).value,
                            }

                            EconomicFactors = {
                                "Z-Score" : sh.cell(row_index, 9 ).value,
                                "Rank" : sh.cell(row_index, 10 ).value,
                            }


                            PhysicalEnvironment = { 
                                "Z-Score" : sh.cell(row_index, 11 ).value,
                                "Rank" : sh.cell(row_index, 12 ).value,
                            }


                            HealthyCounty = {
                                "CountyName" : sh.cell(row_index, 2 ).value,
                                "County FIPS" : sh.cell(row_index, 0 ).value,
                                "QualityofLife": QualityofLife,
                                "HealthBehaviours" : HealthBehaviours,
                                "ClinicalCare" : ClinicalCare,
                                "EconomicFactors" : EconomicFactors,
                                "PhysicalEnvironment" : PhysicalEnvironment
                            }

                            County = {
                                "County" : HealthyCounty
                            }
                            
                            CountyList.append(County)
                    if(row_index == sh.nrows - 1):
                        State = {
                                    "StateName":StateName,
                                    "Year" : yearReported,
                                    "FIPS":sh.cell(row_index, 0 ).value,
                                    "Counties" : CountyList                      
                                }
                        StateList.append(State)
                        # print(State)
        jsonfile = "StateCountyData" + '.json'
        with open(jsonfile, 'w') as f:
            json.dump(StateList, f, indent = 4)
        #connection for local host
        #conn = 'mongodb://localhost:27017'
        #client = pymongo.MongoClient(conn)
        #db=client.heathi_db
        
        #create list of categories.
        Category = ["QualityofLife","EconomicFactors","ClinicalCare","HealthBehaviours","PhysicalEnvironment"]
        #Create a dictionary with the list Category.
        dropdown = {"cat" : Category }

        # Connection for remote host
        ## mongodb://<dbuser>:<dbpassword>@ds255332.mlab.com:55332/healthi_db
        #conn is the mongodb_uri.
        conn = 'mongodb://<dbuser>:<dbpassword>@ds255332.mlab.com:55332/healthi_db'
        client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
        ##rcode client = MongoClient('localhost',27017) # need to find for Heroku
        ##rcode db = client.healthi_db
        ##rcode db = client.Category
        db = client.get_default_database()
         
        #create collection Category
        category = db.Category
        category.drop()
        #insert collection Category.
        category.insert(dropdown)

        #rcode db = client.State
        #drop/create collection State.
        db.State.drop()
        state = db.State
        result = state.insert_many(StateList)
        print("Multiple States {0}".format(result.inserted_ids))
       
        for item in db.State.find():
            # if ('StateName' in item and 'Counties' in item):
            print(item)
        # db.State.find().pretty()
        
JSON_from_excel()

        



