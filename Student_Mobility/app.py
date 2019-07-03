# Import Library Dependencies
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify)

#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
# Import Login Credentials From Config.py File
# from config import user, password


print('\n\tInitializing Flask App...')
app = Flask(__name__)

user = 'root'
password = 'Amazing123'

# Create MySQL Connection String
mysql_uri = f'mysql://{user}:{password}@localhost/student_mobility'
print('\n\t', mysql_uri, '\n')

# Establish Connection to Database
engine = create_engine(mysql_uri, echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
# Base.classes.keys()

# Map Database Models to Variables
Student = Base.classes.students
Record = Base.classes.records
School = Base.classes.schools
Program = Base.classes.programs

# Establish ORM Session For Querying Database
session = Session(bind=engine)


# Create database tables
# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     # db.drop_all()
#     # db.create_all()


@app.route("/")
def render_home():
    """Render Home Page."""
    return render_template("index.html")


@app.route("/graphs")
def render_graphs():
    print('[Python | Reroute] Load Interactive Graph Webpage')
    return render_template('index.html')


@app.route("/timeline")
def render_intro():
    return render_template("timeline.html")


@app.route("/bubbles")
def query_bubbles():
    print('[Python | Query] Get Bubble Data')
    base_query = session.query(
        Record.student_id,
        Record.school_id,
    ).all()

    # Convert Query to Dataframe for Transformation
    query_df = pd.DataFrame(
        base_query,
        columns=['exit_count', 'school_id']
    )
    # Transformation - Groupby
    query_df = query_df.groupby('school_id')['exit_count'] \
        .count() \
        .sort_values(ascending=False) \
        .reset_index()

    # DataFrame Column Division
    query_df['exit_count'] = query_df['exit_count'] \
        .map(lambda x: x / 23)

    print(f"\n\t{query_df}\n")

    # Saving DataFrame Columns as List Variables
    schools = list(query_df['school_id'])
    exit_counts = list(query_df['exit_count'])
    chart_w = (1000 / 2)
    chart_h = (800 / 2)

    # Jsonifying Data For d3 Function Extraction
    trace = {
        "radius": exit_counts,
        "cx": [chart_w for x in exit_counts],
        "cy": [chart_h for x in exit_counts]
    }
    return jsonify(trace)

########################################################
#               [Route] "/default"
########################################################


@app.route("/default")
# @app.route("/emoji_char")
def default_query():
    # Query Database and Transform Data
    print('[Python | Default Query] Count # Students Exit by Month')
    query = session.query(
        Record.leave_date,
        Record.exit_reason
    ).all()

    query_df = pd.DataFrame(
        query,
        columns=['leave_date', 'exit_count']
    )
    query_df['leave_date'] = query_df['leave_date'] \
        .map(lambda x: x.strftime('%Y-%m'))

    query_df = query_df.groupby('leave_date')['exit_count'] \
        .count() \
        .reset_index()
    print(f"\n\t{query_df}\n")

    leave_dates = list(query_df['leave_date'])
    exit_counts = list(query_df['exit_count'])

    #
    trace = {
        "x": leave_dates,
        "y": exit_counts,
        "type": "bar"
    }
    return jsonify(trace)


@app.route("/sample1")
def student_exit_query():
    pass


@app.route("/elim_outliers")
def transform_exclude_may():
    # Trnasform Queried Data to Elimiate Distortion of May
    # Query Database and Transform Data
    print('[Python | Query #2] Eliminate May Distortion')
    query = session.query(
        Record.leave_date,
        Record.exit_reason
    ).all()

    query_df = pd.DataFrame(
        query,
        columns=['leave_date', 'exit_count']
    )
    # Add 'Leave_Month' Column For Sorting & Filtering
    query_df['leave_month'] = query_df['leave_date'] \
        .map(lambda x: x.strftime('%B'))

    # Exclude Month of May To Eliminate Visual Distortion in Graph
    query_df = query_df.loc[query_df['leave_month'] != 'May']

    # Convert Format of Leave Date Column To: Year-Month
    query_df['leave_date'] = query_df['leave_date'] \
        .map(lambda x: x.strftime('%Y-%m'))

    # Group Data By Leave Date & Count Number of Students Exit
    query_df = query_df.groupby('leave_date')['exit_count'] \
        .count() \
        .reset_index()

    # Print Data to Terminal Window
    print(f"\n\t{query_df}\n")

    # Split Data Frame Columns & Render as Lists
    leave_dates = list(query_df['leave_date'])
    exit_counts = list(query_df['exit_count'])

    # Create Export Data Dictionary
    trace = {
        "x": leave_dates,
        "y": exit_counts,
        "type": "bar"
    }
    return jsonify(trace)


if __name__ == '__main__':
    app.run(port=5000, debug=False)
