#-----------------Import Dependencies----------------------------# 
import xlrd
from glob2 import glob
import json
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import string
import re
#--------------------------------------------------------------------------------#
def JSON_from_excel():
        statesOfUSA = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


        filePath = ""
        website_url = requests.get("https://en.wikipedia.org/w/index.php?title=User:Michael_J/County_table&oldid=368803236").text
        wikiBaseURL = "https://en.wikipedia.org"
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
                            Soup = BeautifulSoup(website_url,'lxml')
                            CountyGeoLocTbl = Soup.find('table',{'class':'wikitable sortable'})
                            StateShortName = sh.cell(row_index, 13 ).value
                            CountyName = sh.cell(row_index, 2 ).value
                            
                            StateName = sh.cell(row_index, 1 ).value 

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
                            # Perform lookup from the scraped data for the geo 
                            # locations and other facts
                            # skip the first row of the scraped data as it is the header.
                            for tr in CountyGeoLocTbl.find_all('tr')[1:]:
                                tds = tr.find_all('td')
                                # Removed the superscripts e.g '[4]' with '' by usage of Regex
                                ScrapedCounty = re.compile('[a-zA-Z ]{6,}',re.I).findall(tds[3].text)
                                # Check for blanks / '' in  scraped county
                                if (len(ScrapedCounty)>0):
                                    ScrapedCounty = ScrapedCounty[0].rstrip()
                                    
                                # perform lookup 
                                if(tds[1].text == StateShortName and ScrapedCounty  == CountyName):
                                    CountyWikiLink = wikiBaseURL + tds[3].a.get('href')        
                                    
                                    # Populate the county dictionary
                                    HealthyCounty = {
                                        "CountyName" : CountyName,
                                        "County FIPS" : sh.cell(row_index, 0 ).value,
                                        "QualityofLife": QualityofLife,
                                        "HealthBehaviours" : HealthBehaviours,
                                        "ClinicalCare" : ClinicalCare,
                                        "EconomicFactors" : EconomicFactors,
                                        "PhysicalEnvironment" : PhysicalEnvironment,
                                        "Population" : tds[5].text,
                                        "TotalArea" : tds[11].text,
                                        "Latitude" : tds[12].text.strip(),
                                        "Longitude" : tds[13].text.strip(),
                                        "CountyWikiLink" :CountyWikiLink
                                    }
                                    County = {
                                        "County" : HealthyCounty
                                    }
                                    # Add only when we have found the facts on the county
                                    CountyList.append(County)

                    if(row_index == sh.nrows - 1):
                        State = {
                                    "StateName":StateName,
                                    "StateShortName" : StateShortName,
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
        # db=client.healthi_db
        
        # #Connection for remote host
        conn = 'mongodb://<add user Pwd here>@ds255332.mlab.com:55332/healthi_db'
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
## Updated & Tested Riicha : 9/15/2018 Web Scaped & Added # 1. Lat & Long of counties.2. Link to Wiki 
# 3. population & 4. Area etc

        



