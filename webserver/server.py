#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.

eugene wu 2015
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, jsonify, json 
import sys  
import datetime 
from decimal import Decimal 


reload(sys)  
sys.setdefaultencoding('utf-8')


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db1.cloudapp.net:5432/proj1part2
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db1.cloudapp.net:5432/proj1part2"
#
#DATABASEURI = "sqlite:///test.db"
DATABASEURI = "mysql://sql5103570:QKh89MU44F@sql5.freemysqlhosting.net:3306/sql5103570"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
#engine.execute("""DROP TABLE IF EXISTS test;""")
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
 # id serial,
  #name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


# def bfs_paths(graph, start, goal):
#     queue = [(start, [start])]
#     while queue:
#         (vertex, path) = queue.pop(0)
#         for next in graph[vertex] - set(path):
#             if next == goal:
#                 yield path + [next]
#             else:
#                 queue.append((next, path + [next]))


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a POST or GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
# 
names = []
@app.route('/', methods=["POST", "GET"])
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #

  cursor = g.conn.execute("SHOW TABLES")

  names = []  
  for result in cursor:
    names.append(result[0].decode('unicode_escape').encode('ascii','ignore'))  # can also be accessed using result[0]
  cursor.close()


  # cursor.close()
  # cursor2.close()
  # cursor3.close()

  # cursor = g.conn.execute("SHOW TABLES")
  # tables = cursor.fetchall()
  # cursor.close()
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict( data = names )


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #

  #return render_template("index.html", **context)
  if request.method == "POST": 
    return render_template("index.html", data = names, results = output)
  else:
    return render_template("index.html", data = names)

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another/
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
savedData = []
@app.route('/saved')
def saveData():
  cursor = g.conn.execute("SHOW TABLES")
  names = []  
  for result in cursor:
    names.append(result[0].decode('unicode_escape').encode('ascii','ignore'))  # can also be accessed using result[0]
  cursor.close()
  return render_template("saved.html", data = names, saved = savedData)


@app.route('/saved/<results>')
def saved(results):
  savedData = results
  print savedData
  return "success"


@app.route('/results', methods=['GET'])
def output():
    joinDict = {}
    output = []
    output2 = ""
    tablesArray = []
    joinArray = []
    if request.args.get('resultsValue'):
      keywordList = request.args.get('resultsValue').split()
      keyword = true
    else: 
      keyword = false
    if(keyword != false and len(keywordList) == 1): 
      cursor = g.conn.execute("SHOW TABLES")
      if(cursor.rowcount > 0):
        for r in cursor:
          table = r[0]
          sql_search = "SELECT * FROM " + table + " WHERE "
          sql_search_fields = []
          sql2 = "DESCRIBE " + table
          cursor2 = g.conn.execute(sql2)
          if(cursor2.rowcount > 0):
            for r2 in cursor2:
              colum = r2[0]
              sql_search_fields.append(colum + " LIKE('%%" + keywordList[0] + "%%')")
          clause = ' OR '.join(sql_search_fields)
          sql_search += clause 
          cursor3 = g.conn.execute(sql_search)
          if(cursor3.rowcount != 0):
            tablesObj = {}
            tablesArray.append(tablesObj)
            joinDict[table] = sql_search 
            tablesObj["tableName"] = "<a href='#' class = '" + table + "'>" + table + "</a>" 
            tablesObj["numRows"] = "Number of rows:  " + str(cursor3.rowcount) 
            tableValue = []
            tablesObj["tableData"] = {"value": tableValue, "columns": cursor3.keys()}
            for result in cursor3:
              y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
              tableValue.append(y)
            sql3 = "SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE  REFERENCED_TABLE_NAME = '" + table + "' OR TABLE_NAME = '" + table + "' AND TABLE_SCHEMA = 'sql5103570'"
            cursor4 = g.conn.execute(sql3)
            for r3 in cursor4: 
              #if(r3[2] == 'PRIMARY'):
                #output.append(str(r3[2]) + "," + str(r3[6]))
              if(r3[2] != 'PRIMARY'):
                joinObj = {}
                joinArray.append(joinObj)
                if (r3[5] == table):
                  #output.append(str(r3[2]) + "," + table + "," + str(r3[6]) + "," + str(r3[10]) + "," + str(r3[11]))
                  joinObj["tableName"] = "<a href ='#' class = 'join'>" + table + "JOIN" + str(r3[10]) + "ON" + str(r3[11]) + "</a>"   
                  column1 = "tmp." + str(r3[6])
                  column2 = str(r3[10]) + "." + str(r3[11])
                  #alias1 = column1 + " AS " + "tmp_" + str(r3[6]) + ", "
                  #alias2 = column2 + " AS " + str(r3[10]) + "_" + str(r3[11])
               
                  joinQuery = "SELECT * FROM (" + sql_search + ") AS tmp" + " NATURAL JOIN " + str(r3[10]) 
                  cursor = g.conn.execute(joinQuery)
                  joinObj["numRows"] = "Number of rows: " + str(cursor.rowcount)

                  nullQuery = "SELECT "
                  for item in set(cursor.keys()):
                    nullQuery += "SUM(CASE WHEN " + item + " IS NULL THEN 1 ELSE 0 END) as " + "'Null values for " + item + "', "
                  nullQuery = nullQuery[:-2]
                  nullQuery += " FROM (" + joinQuery + ") AS a"              
                  cursor2 = g.conn.execute(nullQuery)
                  nullValue = []
                  joinObj["nullData"] = {"value": nullValue, "columns": cursor2.keys()}
                  for result in cursor2:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else str(i) if isinstance(i, Decimal) else i) for i in list(result)]
                      nullValue.append(y)
                  uniqueQuery = "SELECT "
                  for item in set(cursor.keys()):
                    uniqueQuery += "COUNT(DISTINCT " + item + ") as 'Unique values for " + item + "', "
                  uniqueQuery = uniqueQuery[:-2]
                  uniqueQuery += "  FROM (" + joinQuery + ") AS a"
                  cursor3 = g.conn.execute(uniqueQuery)
                  uniqueValue = []
                  joinObj["uniqueData"] = {"value": uniqueValue, "columns": cursor3.keys()}
                  for result in cursor3:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else str(i) if isinstance(i, Decimal) else i) for i in list(result)]
                      uniqueValue.append(y)
                  #output.append("Number of null values: " + str(cursor2.fetchone()[0]))
                  
                  tableValue = []
                  joinObj["tableData"] = {"value": tableValue, "columns" : cursor.keys()}
                  counter = 0
                  for result in cursor:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      if counter == 30:
                        break
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else i) for i in list(result)]
                      tableValue.append(y)
                      counter = counter + 1
                  cursor.close()   
                  cursor2.close()  
                  cursor3.close()             
                else:
                  #output.append(str(r3[2]) + "," + table + "," + str(r3[5]) + "," + str(r3[6]))
                  joinObj["tableName"] = "<a href ='#' class = 'join'>" + table + "JOIN" + str(r3[5]) + "ON" + str(r3[6]) + "</a>"
                  column1 = "tmp." + str(r3[6])
                  column2 = str(r3[5]) + "." + str(r3[6])
               
                  joinQuery = "SELECT * FROM (" + sql_search + ") AS tmp" + " NATURAL JOIN " + str(r3[5]) 
                  cursor = g.conn.execute(joinQuery)

                  joinObj["numRows"] = "Number of rows: " + str(cursor.rowcount)
                  nullQuery = "SELECT "
                  for item in set(cursor.keys()):
                    nullQuery += "SUM(CASE WHEN " + item + " IS NULL THEN 1 ELSE 0 END) as " + "'Null values for " + item + "', "
                  nullQuery = nullQuery[:-2]
                  nullQuery += " FROM (" + joinQuery + ") AS a"               
                  cursor2 = g.conn.execute(nullQuery)
                  nullValue = []
                  joinObj["nullData"] = {"value": nullValue, "columns": cursor2.keys()}
                  for result in cursor2:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else str(i) if isinstance(i, Decimal) else i) for i in list(result)]
                      nullValue.append(y)
                  uniqueQuery = "SELECT "
                  for item in set(cursor.keys()):
                    uniqueQuery += "COUNT(DISTINCT " + item + ") as 'Unique values for " + item + "', "
                  uniqueQuery = uniqueQuery[:-2]
                  uniqueQuery += "  FROM (" + joinQuery + ") AS a"
                  cursor3 = g.conn.execute(uniqueQuery)
                  uniqueValue = []
                  joinObj["uniqueData"] = {"value": uniqueValue, "columns": cursor3.keys()}
                  for result in cursor3:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else str(i) if isinstance(i, Decimal) else i) for i in list(result)]
                      uniqueValue.append(y)
                  tableValue = []
                  joinObj["tableData"] = {"value": tableValue, "columns" : cursor.keys()}
                  counter = 0
                  for result in cursor:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      if counter == 30:
                        break 
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else i) for i in list(result)]
                      tableValue.append(y)
                      counter = counter + 1
                  cursor.close()  
                  cursor2.close()
                  cursor3.close()
    elif(len(keywordList) == 2):
      tables_first = []
      tables_second = []
      cursor = g.conn.execute("SHOW TABLES")
      if(cursor.rowcount > 0):
        for r in cursor:
          table = r[0]
          sql_search = "SELECT * FROM " + table + " WHERE "
          sql_search_fields = []
          sql2 = "DESCRIBE " + table
          cursor2 = g.conn.execute(sql2)
          if(cursor2.rowcount > 0):
            for r2 in cursor2:
              colum = r2[0]
              sql_search_fields.append(colum + " LIKE('%%" + keywordList[0] + "%%')")
          clause = ' OR '.join(sql_search_fields)
          sql_search += clause 
          cursor3 = g.conn.execute(sql_search)
          if(cursor3.rowcount != 0):
            tables_first.append(table)
      cursor = g.conn.execute("SHOW TABLES")
      if(cursor.rowcount > 0):
        for r in cursor:
          table = r[0]
          sql_search = "SELECT * FROM " + table + " WHERE "
          sql_search_fields = []
          sql2 = "DESCRIBE " + table
          cursor2 = g.conn.execute(sql2)
          if(cursor2.rowcount > 0):
            for r2 in cursor2:
              colum = r2[0]
              sql_search_fields.append(colum + " LIKE('%%" + keywordList[1] + "%%')")
          clause = ' OR '.join(sql_search_fields)
          sql_search += clause 
          cursor3 = g.conn.execute(sql_search)
          if(cursor3.rowcount != 0):
            tables_second.append(table)
      for element in tables_first:
        table = element
        if table in tables_second: 
          sql_search = "SELECT * FROM " + table + " WHERE "
          sql_search_fields = []
          sql2 = "DESCRIBE " + table
          cursor2 = g.conn.execute(sql2)
          if(cursor2.rowcount > 0):
            for r2 in cursor2:
              colum = r2[0]
              sql_search_fields.append(colum + " LIKE('%%" + keywordList[0] + "%%')")
              sql_search_fields.append(colum + " LIKE('%%" + keywordList[1] + "%%')")
          clause = ' OR '.join(sql_search_fields)
          sql_search += clause 
          cursor3 = g.conn.execute(sql_search)
          if(cursor3.rowcount != 0):
           
            tablesObj = {}
            tablesArray.append(tablesObj)
            joinDict[table] = sql_search 
            
            tablesObj["tableName"] = "<a href='#' class = '" + table + "'>" + table + "</a>" 
            tablesObj["numRows"] = "Number of rows:  " + str(cursor3.rowcount) 
            tableValue = []
            tablesObj["tableData"] = {"value": tableValue, "columns": cursor3.keys()}
            for result in cursor3:
              y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
              tableValue.append(y)
            sql3 = "SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE  REFERENCED_TABLE_NAME = '" + table + "' OR TABLE_NAME = '" + table + "' AND TABLE_SCHEMA = 'sql5103570'"
            cursor4 = g.conn.execute(sql3)
            for r3 in cursor4: 
              if(r3[2] != 'PRIMARY'):
                joinObj = {}
                joinArray.append(joinObj)
                if (r3[5] == table):
                  #output.append(str(r3[2]) + "," + table + "," + str(r3[6]) + "," + str(r3[10]) + "," + str(r3[11]))
                  joinObj["tableName"] = "<a href ='#' class = 'join'>" + table + "JOIN" + str(r3[10]) + "ON" + str(r3[11]) + "</a>"   
                  column1 = "tmp." + str(r3[6])
                  column2 = str(r3[10]) + "." + str(r3[11])
                  #alias1 = column1 + " AS " + "tmp_" + str(r3[6]) + ", "
                  #alias2 = column2 + " AS " + str(r3[10]) + "_" + str(r3[11])
               
                  joinQuery = "SELECT * FROM (" + sql_search + ") AS tmp" + " NATURAL JOIN " + str(r3[10]) 
                  cursor = g.conn.execute(joinQuery)
                  joinObj["numRows"] = "Number of rows: " + str(cursor.rowcount)

                  nullQuery = "SELECT "
                  for item in set(cursor.keys()):
                    nullQuery += "SUM(CASE WHEN " + item + " IS NULL THEN 1 ELSE 0 END) as " + "'Null values for " + item + "', "
                  nullQuery = nullQuery[:-2]
                  nullQuery += " FROM (" + joinQuery + ") AS a"              
                  cursor2 = g.conn.execute(nullQuery)
                  nullValue = []
                  joinObj["nullData"] = {"value": nullValue, "columns": cursor2.keys()}
                  for result in cursor2:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else str(i) if isinstance(i, Decimal) else i) for i in list(result)]
                      nullValue.append(y)
                  uniqueQuery = "SELECT "
                  for item in set(cursor.keys()):
                    uniqueQuery += "COUNT(DISTINCT " + item + ") as 'Unique values for " + item + "', "
                  uniqueQuery = uniqueQuery[:-2]
                  uniqueQuery += "  FROM (" + joinQuery + ") AS a"
                  cursor3 = g.conn.execute(uniqueQuery)
                  uniqueValue = []
                  joinObj["uniqueData"] = {"value": uniqueValue, "columns": cursor3.keys()}
                  for result in cursor3:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else str(i) if isinstance(i, Decimal) else i) for i in list(result)]
                      uniqueValue.append(y)
                  #output.append("Number of null values: " + str(cursor2.fetchone()[0]))
                  
                  tableValue = []
                  joinObj["tableData"] = {"value": tableValue, "columns" : cursor.keys()}
                  counter = 0
                  for result in cursor:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      if counter == 30:
                        break
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else i) for i in list(result)]
                      tableValue.append(y)
                      counter = counter + 1
                  cursor.close()   
                  cursor2.close()  
                  cursor3.close()               
                else:
                  #output.append(str(r3[2]) + "," + table + "," + str(r3[5]) + "," + str(r3[6]))
                  joinObj["tableName"] = "<a href ='#' class = 'join'>" + table + "JOIN" + str(r3[5]) + "ON" + str(r3[6]) + "</a>"
                  column1 = "tmp." + str(r3[6])
                  column2 = str(r3[5]) + "." + str(r3[6])
               
                  joinQuery = "SELECT * FROM (" + sql_search + ") AS tmp" + " NATURAL JOIN " + str(r3[5]) 
                  cursor = g.conn.execute(joinQuery)

                  joinObj["numRows"] = "Number of rows: " + str(cursor.rowcount)
                  nullQuery = "SELECT "
                  for item in set(cursor.keys()):
                    nullQuery += "SUM(CASE WHEN " + item + " IS NULL THEN 1 ELSE 0 END) as " + "'Null values for " + item + "', "
                  nullQuery = nullQuery[:-2]
                  nullQuery += " FROM (" + joinQuery + ") AS a"               
                  cursor2 = g.conn.execute(nullQuery)
                  nullValue = []
                  joinObj["nullData"] = {"value": nullValue, "columns": cursor2.keys()}
                  for result in cursor2:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else str(i) if isinstance(i, Decimal) else i) for i in list(result)]
                      nullValue.append(y)
                  uniqueQuery = "SELECT "
                  for item in set(cursor.keys()):
                    uniqueQuery += "COUNT(DISTINCT " + item + ") as 'Unique values for " + item + "', "
                  uniqueQuery = uniqueQuery[:-2]
                  uniqueQuery += "  FROM (" + joinQuery + ") AS a"
                  cursor3 = g.conn.execute(uniqueQuery)
                  uniqueValue = []
                  joinObj["uniqueData"] = {"value": uniqueValue, "columns": cursor3.keys()}
                  for result in cursor3:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else str(i) if isinstance(i, Decimal) else i) for i in list(result)]
                      uniqueValue.append(y)
                  tableValue = []
                  joinObj["tableData"] = {"value": tableValue, "columns" : cursor.keys()}
                  counter = 0
                  for result in cursor:
                      #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
                      if counter == 30:
                        break 
                      y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else i) for i in list(result)]
                      tableValue.append(y)
                      counter = counter + 1
                  cursor.close()  
                  cursor2.close()
                  cursor3.close()
      output.append("<br>Joins that contain both keywords: <br>")
      for element in tables_first:
          table = element
          if table not in tables_second: 
            sql3 = "SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE  REFERENCED_TABLE_NAME = '" + table + "' OR TABLE_NAME = '" + table + "' AND TABLE_SCHEMA = 'sql5103570'"
            cursor3 = g.conn.execute(sql3)
            for r3 in cursor3: 
              if(r3[2] != 'PRIMARY'):
                if (r3[5] == table):
                  if str(r3[10]) in tables_second: 
                    #output.append(str(r3[2]) + "," + table + "," + str(r3[10]) + "," + str(r3[11]))
                    output.append("<a href ='#' class = 'join'>" + table + "JOIN" + str(r3[10]) + "ON" + str(r3[11]) + "</a>")                     
                else:
                  if str(r3[5]) in tables_second: 
                    #output.append(str(r3[2]) + "," + table + "," + str(r3[5]) + "," + str(r3[6]))
                    output.append("<a href ='#' class = 'join'>" + table + "JOIN" + str(r3[5]) + "ON" + str(r3[6]) + "</a>") 


    ret_data = {"tables": tablesArray, "joins": joinArray, "query": joinDict}
    sortArray = ret_data["joins"]
    for i in range(0, len(sortArray)):
      initialNum = [int(s) for s in sortArray[i]["numRows"].split() if s.isdigit()]
      minValue = initialNum[0]
      minIndex = i
      for j in range(i, len(sortArray)):
          num2 = [int(s) for s in sortArray[j]["numRows"].split() if s.isdigit()]
          if minValue > num2[0]:
            minValue = num2[0]
            minIndex = j
      print minValue 
      sortArray[i], sortArray[minIndex] = sortArray[minIndex], sortArray[i]
   
    #ret_data = {"value": output, "query": joinDict}
    return jsonify(ret_data)

@app.route('/tableData', methods=["POST",'GET'])
def tableData():
  id = request.json['json_str']
  cursor = g.conn.execute("SELECT * FROM " + id)
  columns = cursor.keys()
  rowData = []  
  for result in cursor:
    #customers.append(result[0].decode('unicode_escape').encode('ascii','ignore'))  # can also be accessed using result[0]
    #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
    y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else i) for i in list(result)]
    rowData.append(y)
  cursor.close()
  ret_data = {"value": rowData, "columns" : columns}
  return jsonify(ret_data)

@app.route('/joinData', methods=["POST",'GET'])
def joinData():
  joinInfo = request.json['json_str']
  keyword = request.json['keyword']
  query = request.json['json_dict']
  splitArr = joinInfo.split("ON",1)
  table1 = splitArr[0].split("JOIN",1)[0]
  table2 = splitArr[0].split("JOIN",1)[1]
  #column1 = table1 + "." + splitArr[1]
  column1 = "tmp." + splitArr[1]
  column2 = table2 + "." + splitArr[1]
  
  queryForCursor = "SELECT * FROM " + "(" + query[table1] + ") AS tmp" + " NATURAL JOIN " + table2 
  cursor = g.conn.execute(queryForCursor)
  columns = cursor.keys()
  rowData = []  
  for result in cursor:
    #y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
    y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else (i.strftime('%m/%d/%Y') if isinstance(i, datetime.date) else i) for i in list(result)]
    rowData.append(y)
  cursor.close()
  
  ret_data = {"value": rowData, "columns" : columns}
  return jsonify(ret_data)
# @app.route('/employees', methods=['GET'])
# def employees():
#   cursor = g.conn.execute("SELECT * FROM employees")
#   employees = []  
#   for result in cursor:
#     #customers.append(result[0].decode('unicode_escape').encode('ascii','ignore'))  # can also be accessed using result[0]
#     y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
#     employees.append(y)
#   cursor.close()
#   ret_data = {"value": employees}
#   return jsonify(ret_data)

# @app.route('/offices', methods=['GET'])
# def offices():
#   cursor = g.conn.execute("SELECT * FROM offices")
#   offices = []  
#   for result in cursor:
#     #customers.append(result[0].decode('unicode_escape').encode('ascii','ignore'))  # can also be accessed using result[0]
#     y = [i.decode('latin-1').encode("utf-8") if isinstance(i, basestring) else i for i in list(result)]
#     offices.append(y)
#   cursor.close()
#   ret_data = {"value": offices}
#   return jsonify(ret_data)
  
# @app.route('/search', methods=["POST", "GET"])
# def search():
#   return render_template("search.html", **context)

if __name__ == "__main__":
  import click
  
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
