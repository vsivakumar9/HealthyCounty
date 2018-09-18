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
# db = client.HealthDB

#------------------------------------------------------------------------------------#
# MLab MongoDB connection #
#------------------------------------------------------------------------------------#
# conn = 'mongodb://healthi_admin:healthisrs9=@ds255332.mlab.com:55332/healthi_db'
# client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)

# #Database connection
# db = client.get_default_database()
# db = client.get_database('healthi_db')

# Home Page
@app.route("/")
def home():
    return(render_template("Landing.html"))

# Route to display all the five attributes to measure health of a county
@app.route("/attributes")
def attributes():
    sample_list = []
    db = client.Category
    for item in db.Category.find():
        for cat in item['cat']:
            sample_list.append(cat)
    return jsonify(sample_list)

#Route to display all the states present in the database
@app.route("/states")
def state():
    sample_list = []
    states_list = []
    Statedict={}
    db = client.State
    for item in db.State.find():
        states_list.append(item['StateName'])
    Statedict['States'] = states_list 
    sample_list.append(Statedict)
    return jsonify(sample_list)  

#Route to display the county names of all the counties present in the given state
@app.route("/countynames/<state>")
def county(state):
    sample_list = []
    db = client.State
    for item in db.State.find():
        county_list=[]
        County_dict={}
        if item['StateName'].lower() == state.lower():
            State_Counties = item['Counties']
            for County in State_Counties:
                county_list.append(County['County']['CountyName'])
            County_dict['County Names'] = county_list          
            sample_list.append({state.upper() : County_dict})
    return jsonify(sample_list)   

#Route to display all the zscores and rank of all the counties for the given state
@app.route("/zscores/<state>")
def zscore(state):
    sample_list = []
    db = client.State
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

# Route to display the all the information about the given state    
@app.route("/details/<state>")
def details(state):
    sample_list = []
    db = client.State
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
#Tested mlab cloud mongodb as well as with local mongodb.    