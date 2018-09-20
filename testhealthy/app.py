import pymongo 
from flask import(Flask, render_template,jsonify)

#------------------------------------------------------------------------------------#
# Flask Setup #
#------------------------------------------------------------------------------------#
app = Flask(__name__)

#------------------------------------------------------------------------------------#
# Local MongoDB connection #
#------------------------------------------------------------------------------------#
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)

# # create / Use database
# # db = client.healthi_db

#------------------------------------------------------------------------------------#
# MLab MongoDB connection #
#------------------------------------------------------------------------------------#
conn = 'mongodb://healthi_admin:healthisrs9=@ds255332.mlab.com:55332/healthi_db'
client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)

# #Database connection
db = client.get_default_database()
# db = client.get_database('healthi_db')


# Home Page
@app.route("/")
def home():
    return(render_template("Landing.html"))

# Route to display all the five attributes to measure health of a county
@app.route("/routes")
def routes():
    sample_list = []
    Routes_dict = {}
    Routes_dict['Attributes'] = "/attributes"
    Routes_dict['States']= "/states"
    Routes_dict['State County Names']="/countynames/<state>"
    Routes_dict['State Zscores Countywise'] ="/countyzscores/<state>"
    Routes_dict['State Details Countywise']="/countyalldetails/<state>"
    Routes_dict['State Geographical & Demographical Details Countywise'] = "/countygeodetails/<state>"
    Routes_dict['Ranks & Zscores Details Countywise'] = "/countyrankszscores/<state>"
    sample_list.append(Routes_dict)
    return jsonify(sample_list)

# Route to display all the five attributes to measure health of a county
@app.route("/attributes")
def attributes(): 
    sample_list = []
    for item in db.Category.find():
        for cat in item['cat']:
            sample_list.append(cat)
    return jsonify(sample_list)

# Route to display all the ranks to measure health of a county
@app.route("/countyrankszscores/<state>")
def rankszscores(state):
    sample_list = []
    County_dict = {}
    for item in db.CountyRanksZscores.find():
        if item['State'].lower() == state.lower():
            County_dict[state.upper()] = item['CountyDetails']
    sample_list.append(County_dict)    
    return jsonify(sample_list)    

#Route to display all the states present in the database
@app.route("/states")
def state():
    sample_list = []
    states_list = []
    Statedict={}
    for item in db.State.find():
        states_list.append(item['StateName'])
    Statedict['States'] = states_list 
    sample_list.append(Statedict)
    return jsonify(sample_list)  

#Route to display the county names of all the counties present in the given state
@app.route("/countynames/<state>")
def county(state):
    sample_list = []
    for item in db.State.find():
        county_list=[]
        County_dict={}
        if item['StateName'].lower() == state.lower():
            State_Counties = item['Counties']
            for County in State_Counties:
                county_list.append(County['County']['CountyName'])
            County_dict['CountyNames'] = county_list          
            sample_list.append(County_dict)
    return jsonify(sample_list)   

#Route to display all the zscores and rank of all the counties for the given state
@app.route("/countyzscores/<state>")
def zscore(state):
    sample_list = []
    for item in db.State.find():
        if item['StateName'].lower() == state.lower():
            State_Counties = item['Counties']
            for Zscores in State_Counties:              
                sample_list.append({Zscores['County']['CountyName']:{
                    "QualityofLife":Zscores['County']['QualityofLife'],
                    "HealthBehaviours":Zscores['County']['HealthBehaviours'],
                    "ClinicalCare" : Zscores['County']['ClinicalCare'], 
                    "EconomicFactors" : Zscores['County']['EconomicFactors'],
                    "PhysicalEnvironment":Zscores['County']['PhysicalEnvironment']
                }})
    return jsonify(sample_list)            

# Route to display the all the geographical & demographics information about the county in the given state  
@app.route("/countygeodetails/<state>")
def geodemo(state):
    sample_list=[]
    for item in db.State.find():
        if item['StateName'].lower() == state.lower():
            State_Counties = item['Counties']
            print(State_Counties)
            for geodemo in State_Counties:
                sample_list.append({geodemo['County']['CountyName']:{  
                'Latitude' : geodemo['County']['Latitude'],
                'Longitude' : geodemo['County']['Longitude'],
                'TotalArea' : geodemo['County']['TotalArea'],
                'Population' : geodemo['County']['Population'],
                'geodemo.CountyWikiLink' : geodemo['County']['CountyWikiLink']
                }})
    return jsonify(sample_list)            

# Route to display the all the information about the given state    
@app.route("/countyalldetails/<state>")
def details(state):
    sample_list = []
    for item in db.State.find():
        Statedetaildict = {}
        if item['StateName'].lower() == state.lower():
            Statedetaildict['State'] = item['StateName']
            Statedetaildict['Year'] = item['Year']
            Statedetaildict['FIPS'] = item['FIPS']
            Statedetaildict['Counties'] = item['Counties']
            sample_list.append(Statedetaildict)
    return jsonify(sample_list)        

#------------------------------------------------------------------------------------#
# Initiate Flask app
#------------------------------------------------------------------------------------#
if __name__=="__main__":
    connect_args={'check_same_thread':False}
    app.run(debug=True)

#Pragati : 9/14/2018. Updated to create 4 routes and modified 1 route.
#          Tested mlab cloud mongodb as well as with local mongodb.  
#Pragati : 9/15/2018. Updated the code and included two routes: /routes to display
#          all the available routes and /countygeodetails/<state> to display
#          geographical & demographical information.
#Supriya : 9/17/2018. Updated line #79 for Java Script Logic; # 42 for correct display 
#          of county details route.
#Pragati : 9/19/2018. Updated the code and included one route: 
#          /countyrankszscores/<state> to display the ranks and zscores of
#          the counties.