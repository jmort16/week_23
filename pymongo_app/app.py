from flask import Flask, render_template, send_file, request
import os
import pymongo
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

#setup mongo connection with database
app.config['MONGO_URI']="mongodb://localhost:27017/shows_db"
mongo = PyMongo(app)

#connect to collection
tv_shows = mongo.db.tv_shows

# Homepage
@app.route("/")
def index():
    #find all items in db and save to a variable
    all_shows = list(tv_shows.find())
    return render_template('index.html',data=all_shows)
    
# Create a record
@app.route("/record_creation",methods=['GET','POST'])
def get_info():
    if request.method == 'GET':
        form_url = os.path.join("templates","create.html")
        # the send_file function lets us send the contents in the form to a client
        return send_file(form_url)
    elif request.method == 'POST':
        show_name = request.form['show_name']
        seasons = request.form['seasons']
        duration = request.form['duration']
        year = request.form['year']
        post_data = {'name':show_name,
                    'seasons':seasons,
                    'duration':duration,
                    'year':year,
                    'date_added':datetime.datetime.utcnow()
        }
        tv_shows.insert_one(post_data)
        text = "New Show Record Created Successfully"
        return text

# Update a record
@app.route("/record_update",methods=['GET','POST'])
def change_info():
    if request.method == 'GET':
        return render_template("update.html")
    else:
        newname = request.form['newname']
        newfield = request.form['newfield']
        newinfo = request.form['newinfo']
        filter = { 'name': newname }
        
        # Values to be updated.
        if newfield == 'NS':
            newvalues = { "$set": { 'Number of Seasons': newinfo } }
        elif newfield == 'EL':
            newvalues = { "$set": { 'Episode Length (in minutes)': newinfo } }
        else:
            newvalues = { "$set": { 'Year Series Began': newinfo } }

        tv_shows.update_one(filter, newvalues)
        text = "Show Record Updated Successfully"
        return text




#READ
if __name__ == "__main__":
    app.run(debug=True)
# Now, we can run this by going to terminal and cd-ing into flaskAPI_framework.
# And run the flask command:
    # we are exporting our flask app to what we called our flask app: 'flask-app'
#      export FLASK_APP=flask-app
    # then we connect to our localhost thru 'flask run'
#      flask run














