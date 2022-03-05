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
@app.route("/record_create",methods=['GET','POST'])
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
        text = "<p>Show Record Created Successfully</p>"
        return text

results= tv_shows.find()
for result in results:
    print(result)

# Update a record
@app.route("/record_update",methods=['GET','POST'])
def change_info():
    if request.method == 'GET':
        return render_template("update.html")
    else:
        update_info = request.form
        newname = update_info['newname']
        newfield = update_info['newfield']
        newinfo = update_info['newinfo']
        filter = { 'name': newname }

        # Values to be updated.
        if newfield == 'NS':
            newvalues = { "$set": { 'seasons': newinfo,
            'date_updated':datetime.datetime.utcnow() }}
        elif newfield == 'EL':
            newvalues = { "$set": { 'duration': newinfo,
            'date_updated':datetime.datetime.utcnow() }}
        elif newfield == 'YB':
            newvalues = { "$set": { 'year': newinfo,
            'date_updated':datetime.datetime.utcnow() }}
        else:
            text = "<p>Enter an option listed.</p>"
            return text

        tv_shows.update_one(filter, newvalues)
        text = "<p>Show Record Updated Successfully</p>"
        return text

# Delete a record
@app.route("/record_delete", methods=["GET", "POST"])

def delete_info():
    if request.method=="GET":
        
        return render_template("delete.html")
    
    else:
                       
        post_delete = {'name':request.form['targetname']}

        tv_shows.delete_one(post_delete)

        return "<p>Show Record Deleted Successfully.</p>"
        
if __name__ == "__main__":
    app.run(debug=True)












