#-----------------Import Dependencies----------------------------# 
import xlrd
from  import glob
import json
import pymongo
from pymongo import MongoClient
#--------------------------------------------------------------------------------#
def JSON_from_excel():
        filePath = ""glob2
        xlsFilesOnly = glob(filePath+"*.xls") # parse all xls file(s) only
        StateList = []
        for xlsfile in xlsFilesOnly:
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
        
        #Creating a json file to display the jsonified data                
        jsonfile = "StateCountyData" + '.json'
        with open(jsonfile, 'w') as f:
            json.dump(StateList, f, indent = 4)

        #Connection for local host
        # conn = 'mongodb://localhost:27017'
        # client = pymongo.MongoClient(conn)
        # db=client.heathi_db
        
        #Connection for remote host
        conn = 'mongodb://<dbuser>:<dbpassword>@ds255332.mlab.com:55332/healthi_db'
        client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
        db = client.get_default_database()

        #create list of categories
        Category = ["QualityofLife","EconomicFactors","ClinicalCare","HealthBehaviours","PhysicalEnvironment"]
        #Create a dictionary with the list Category.
        dropdown = {"cat" : Category }

        #drop/create collection Category
        db.Category.drop()
        category = db.Category
        #insert into Category collection
        category.insert(dropdown)

        #drop/create collection State.
        db.State.drop()
        state = db.State
        #insert into State collection
        result = state.insert_many(StateList)
        print("Multiple States {0}".format(result.inserted_ids))
        
JSON_from_excel()

#Siva : 9/13/2018. Updated to create one database and use the mlab cloud mongodb.
#Pragati : 9/14/2018. Updated and cleaned the code (Note: Verified by re-running the code
#          locally. 
#          Note: Did all this at this state to avoid any last minutes bug & error.


        



