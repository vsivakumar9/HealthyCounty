# modules to interact with mongoDB
import pymongo # runs on 27017
#modules to use flask
from flask import(Flask, render_template, jsonify)

#------------------------------------------------------------------------------------#
# Flask Setup #
#------------------------------------------------------------------------------------#
app = Flask(__name__)

#Server DB connection
conn = 'mongodb://<dbuser>:<dbpassword>@ds255332.mlab.com:55332/healthi_db'
client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)

db = client.get_default_database()
# db = client.get_database('healthi_db')

#Local DB connection
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)

# create / Use database
# db = client.HealthDB

# Home Page --> Render Landing.html from template
@app.route("/")
def home():
    return(render_template("Landing.html"))

@app.route("/attributes")
def attributes():
    # print("Names invoked")
    # Get the sample list which is the column names in Samples table 
    sample_list = []
    for item in db.Category.find():
        for cat in item['cat']:
            sample_list.append(cat)
    return jsonify(sample_list)

@app.route("/states")
def state():
    sample_list = []
    for item in db.State.find():
        Statedict={}
        Statedict['State'] = item['StateName']                
        sample_list.append(Statedict)
    return jsonify(sample_list)  

@app.route("/countynames/<state>")
def county(state):
    sample_list = []
    for item in db.State.find():
        Countydict={}
        if item['StateName'].lower() == state.lower():
            Countydict['Counties'] = item['Counties']              
            sample_list.append(Countydict)
    return jsonify(sample_list)        

# Route to display the state specific information    
@app.route("/details/<state>")
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
        print(sample_list)    
    return jsonify(sample_list)        
#------------------------------------------------------------------------------------#
# Initiate Flask app
#------------------------------------------------------------------------------------#
if __name__=="__main__":
    connect_args={'check_same_thread':False}
    app.run(debug=True)