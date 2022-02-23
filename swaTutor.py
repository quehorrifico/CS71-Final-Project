from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
import sqlite3
import hashlib
import re


app = Flask(__name__)

# set secret key
app.secret_key = 'CS71-SWAT-520493820'

# Hashing
def myHashFunction(data):
    hash = hashlib.sha256(data.encode())
    return hash.hexdigest()

# Login helper functions
def isLoggedIn():
    return "username" in session and session["username"] != ""

def getisprof():
    setisprof()
    return session["isprof"]

def setisprof():
    data = getUsers()
    for i in range(len(data)):
        if getCurrentUsername() == data[i][1]:
            session["isprof"] = str(data[i][3])

def getCurrentUsername():
    return session["username"]

def setCurrentUsername(username):
    session["username"] = username

def attemptLogout():
    session["username"] = ""
    return True

def attemptLogin(username, password):
    hash = myHashFunction(password)
    if validate(username, hash):
        setisprof()
        setCurrentUsername(username)
        return True
    else:
        return False

def validate(username, hash):
    # conn = sqlite3.connect('private/swatutor.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM users;")
    # data = cursor.fetchall()
    data = getUsers()
    for i in range(len(data)):
        if username == data[i][1]:
            if hash == data[i][2]:
                # conn.commit()
                # conn.close()
                return True
    else:
        # conn.commit()
        # conn.close()
        return False

# Registration helper functions
def isEmailValid(email):
    if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return True
    else:
        return False

def isUsernameValid(username):
    length = len(username)
    if username.isalnum() and length > 0 and length < 256:  #can update required min/max length
        return True
    else:
        return False

def isPasswordValid(password):
    # Minimum 8 and maximum 20 characters, at least one uppercase letter,
    # one lowercase letter, one number and one special character:
    if re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$", password):
        return True
    else:
        return False

def isUsernameAvailable(username):
    data = getUsers()
    for i in range(len(data)):
        if username == data[i][1]:
            return False
    else:
        return True

def getUsers():
    #email, user, pass, id_prof, is_tutor, course
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

#implement table
def getFeedback():
    #time, feedback, username
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback;")
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def setFeedback(time, feedback, username):
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    sql_command = 'insert into feedback (time,feedback,username) values ("' + time + '","' + feedback + '","' + username + '");'
    cursor.execute(sql_command)
    conn.commit()
    conn.close()

def getRequest():
    #username, coursereq, timeofrequest, tutorassigned (int), tutorname
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests;")
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data


def getTutors():
    #tutor_name, course, availability
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tutors;")
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def setRequests(username, department, courseRequest, timeOfRequest, tutorAssigned):
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    #print(tutorassigned)
    sql_command = 'insert into requests (username,department,courseRequest,timeOfRequest,tutorAssigned) values ("' + username + '","' + department + '","' + courseRequest + '","' + timeOfRequest + '","' + str(tutorAssigned) + '");'
    cursor.execute(sql_command)
    conn.commit()
    conn.close()

# New one
def getCourses():
    #department, course
    f = open("courses.txt", "r")


def getCourses():
    #department, course
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses;")
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def registerNewUser(email, username, password):
    hash = myHashFunction(password)
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    isprof = "0"
    sql_command = 'insert into users (email,username,hash,isprof) values ("' + email + '","' + username + '","' + hash + '","' + isprof + '");'
    cursor.execute(sql_command)
    conn.commit()
    conn.close()

def addNewTutor(name, course):
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    isAvailable = "1"
    sql_command = 'insert into tutors (name,course) values ("' + name + '","' + course + '");'
    cursor.execute(sql_command)
    conn.commit()
    conn.close()


def assignTutor(student, tutor,course):
    conn = sqlite3.connect('private/swatutor.db')
    cursor = conn.cursor()
    sql_command1 = 'UPDATE tutors SET student = "' +student + '" WHERE name = "' + tutor + '";'
    sql_command2 = 'UPDATE requests SET tutorName = "' +tutor + '" WHERE username = "' + student + '"AND courseRequest = "'+ course +'";'
    sql_command3 = 'UPDATE requests SET tutorAssigned = "1" WHERE username = "' + student + '"AND courseRequest = "'+ course +'";'
    cursor.execute(sql_command1)
    cursor.execute(sql_command2)
    cursor.execute(sql_command3)
    conn.commit()
    conn.close()

# Routing
@app.route("/")
def home():
    if isLoggedIn():
        return redirect(url_for("reqTutor"))
    else:
        return render_template("login.html")

# Eventually gonna have to add functionality here
@app.route("/stud/reqtutor")
def reqTutor():
    if getisprof() != "0":
        return redirect(url_for("profrequests"))
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    return render_template("stud_dash_req_tutor.html",username=username)

# @app.route("/stud/reqtutor/department/<departmentreq>")
# def department(departmentreq):
#     if getisprof() != "0":
#         return redirect(url_for("/prof/allrequests"))
#
#     toReturn = ""
#     #Example for rn
#     courses = {"CPSC":['CPSC course 1','CPSC course 2','CPSC course 3','CPSC 021'],
#     "ENGR":['ENGR course 1','ENGR course 2','ENGR course 3']}
#     coursesToReturn = courses[departmentreq]
#
#     for course in coursesToReturn:
#         toReturn += "<option value =\"" + course +"\">" +course+ "</option>"
#
#     return toReturn

# New one
@app.route("/stud/reqtutor/department/<departmentreq>")
def department(departmentreq):
    if getisprof() != "0":
        return redirect(url_for("profrequests"))

    toReturn = ""
    f = open("courses.txt", "r")

    total = int(f.readline())
    courses = {}
    for i in range(total):
        dept = f.readline()
        course_list = f.readline()
        course_list = course_list.split(",")
        courses[dept[:-1]] = course_list[:-1]
    app.logger.info(courses.keys())
    #courses = {"CPSC":['CPSC course 1','CPSC course 2','CPSC course 3','CPSC 021'],
    #"ENGR":['ENGR course 1','ENGR course 2','ENGR course 3']}
    coursesToReturn = courses[departmentreq]

    for course in coursesToReturn:
        toReturn += "<option value =\"" + course +"\">" +course+ "</option>"

    return toReturn

@app.route("/prof/addtutor/department/<departmentreq>")
def add_tutor_department(departmentreq):
    if getisprof() == "0":
        return redirect(url_for("reqTutor"))

    toReturn = ""
    # This could be optimized
    f = open("courses.txt", "r")
    total = int(f.readline())

    courses = {}
    for i in range(total):
        dept = f.readline()
        course_list = f.readline()
        course_list = course_list.split(",")
        courses[dept[:-1]] = course_list[:-1]
    app.logger.info(courses.keys())
    #courses = {"CPSC":['CPSC course 1','CPSC course 2','CPSC course 3','CPSC 021'],
    #"ENGR":['ENGR course 1','ENGR course 2','ENGR course 3']}
    coursesToReturn = courses[departmentreq]

    for course in coursesToReturn:
        toReturn += "<option value =\"" + course +"\">" +course+ "</option>"

    return toReturn

@app.route("/stud/feedback")
def studFeedback():
    if getisprof() != "0":
        return redirect(url_for("profrequests"))
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    return render_template("stud_dash_feedback.html",username=username)

@app.route("/stud/pending")
def studPending():
    if getisprof() != "0":
        return redirect(url_for("profrequests"))
    # Test values for right now, TODO: get correct data about pending requests sent forward
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    #pending_requests = [('CPSC','CPSC021','April 18, 2021','Submitted'),('CPSC','CPSC071','April 17, 2021','Submitted')]
    data = getRequest()
    pending_requests = []
    for i in range(len(data)):
        if data[i][0] == username:
            if data[i][4] == "0":
                status = "In Progress"
            else:
                status = "Tutor Assigned"
            pending_requests.append((data[i][1],data[i][2],data[i][3],status))

    if len(pending_requests) > 0:
        return render_template("stud_dash_pend_req.html",len = len(pending_requests),pending_requests=pending_requests,username=username)
    else:
        return render_template("stud_dash_pend_req.html",len = len(pending_requests),pending_requests="You have no pending requests",username=username)

@app.route("/stud/request")
def studRequest():
    if getisprof() != "0":
        return redirect(url_for("profrequests"))
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    return render_template("stud_dash_req_tutor.html",username=username)

@app.route("/prof/allrequests")
def profrequests():
    if getisprof() == "0":
        return redirect(url_for("reqTutor"))
    # Test values for right now, TODO: get correct data about all requests sent forward
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    students = []

    data = getRequest()
    all_requests = []
    for i in range(len(data)):
        if data[i][4] == "0":
            status = "Need to assign tutor"
            students.append(data[i][0]+"_"+data[i][2])
        else:
            status = "Tutor Assigned"
        all_requests.append((data[i][0],data[i][1],data[i][2],data[i][3],status))
        # would want a way to deal with multiple requests from same user

    #all_requests = [('John Doe','CPSC','CPSC021','April 18, 2021','Submitted'),('Jane Doe','CPSC','CPSC071','April 17, 2021','Submitted')]
    if all_requests:
        return render_template("prof_dash_all_requests.html",len = len(all_requests),all_requests=all_requests,username=username,students=students)
    else:
        return render_template("prof_dash_all_requests.html",len = len(all_requests),all_requests='There are no requests made',username=username,students=students)

@app.route("/prof/allrequests/whichtutors/<student_course>")
def whichtutors(student_course):
    if getisprof() == "0":
        return redirect(url_for("reqTutor"))

    toReturn = ""


    app.logger.info(student_course)
    course = student_course.split("_")[1]
    app.logger.info(course)

    tutorsToReturn = []
    tutors = getTutors();
    for row in tutors:
        if course == row[1] and row[2] == None:
            tutorsToReturn.append(row[0])


    for tutor in tutorsToReturn:
        toReturn += "<option value =\"" + tutor +"\">" +tutor+ "</option>"

    return toReturn


@app.route("/tutor_assign", methods=['POST'])
def tutor_assign():
    if getisprof() == "0":
        return redirect(url_for("reqTutor"))
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    student_course = request.form['student']
    student,course = student_course.split('_')[0],student_course.split('_')[1]
    tutor = request.form['tutor']

    # We have the tutorName,department, and course
    app.logger.info(student)
    app.logger.info(tutor) #remove
    app.logger.info(course)


    assignTutor(" "+student, tutor,course)

    # For recording time of feedback given
    return redirect(url_for("profrequests"))
    # if (student != "" and tutor!=""):
    #     return render_template("prof_dash_all_requests.html",assigned_feedback='Tutor Added!',username=username)
    # else:
    #     return render_template("prof_dash_all_requests.html",assigned_feedback='Please Fill Out All Information',username=username)

@app.route("/prof/addtutor")
def profAdd():
    if getisprof() == "0":
        return redirect(url_for("reqTutor"))
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    return render_template("prof_dash_add_tutor.html",username=username)

@app.route('/prof/addtutor/newtutor', methods=['POST'])
def handle_data():
    if getisprof() == "0":
        return redirect(url_for("reqTutor"))
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    try:
        tutorName = request.form['tutorName']
        department = request.form['department']
        course = request.form['course']
    except:
        return render_template("prof_dash_add_tutor.html",feedback_recorded='Please Fill Out All Information',username=username)

    # We have the tutorName,department, and course
    app.logger.info(tutorName)
    app.logger.info(department) #remove
    app.logger.info(course)

    addNewTutor(tutorName, course)

    # For recording time of feedback given
    request_time = datetime.now()
    app.logger.info(request_time)

    if (tutorName != "" and department!="" and course!=""):
        return render_template("prof_dash_add_tutor.html",feedback_recorded='Tutor Added!',username=username)
    else:
        return render_template("prof_dash_add_tutor.html",feedback_recorded='Please Fill Out All Information',username=username)

@app.route("/prof/alltutors")
def profAll():
    if getisprof() == "0":
        return redirect(url_for("reqTutor"))
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""


    data = getTutors()
    all_tutors = []
    for i in range(len(data)):
        if data[i][2] == None:
            students = "No Students Assigned"
        else:
            students = data[i][2]
        all_tutors.append((data[i][0],data[i][1],students))

    # all_tutors = [('Bob','CPSC021','John Doe'),('Jen','CPSC071','Jane Doe')] #Call function here to actually grab data from db
    if all_tutors:
        return render_template("prof_dash_all_available.html",len=len(all_tutors),all_tutors=all_tutors,username=username)
    else:
        return render_template("prof_dash_all_available.html",len=len(all_tutors),all_tutors="There are no tutors available",username=username)


@app.route("/prof/feedback")
def profFeedback():
    if getisprof() == "0":
        return redirect(url_for("reqTutor"))

    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    # all_feedback gets a database return from feedback table
    data = getFeedback()
    all_feedback = []
    for i in range(len(data)):
        #data[i][0]
        #allFeedback.append(data[i][1])
        all_feedback.append((data[i][2],data[i][0],data[i][1]))

    if all_feedback:
        return render_template("prof_dash_feedback.html",len=len(all_feedback),all_feedback=all_feedback,username=username)
    else:
        return render_template("prof_dash_feedback.html",len=len(all_feedback),all_feedback="There is no feedback",username=username)

@app.route("/tutorRequestProcessing", methods=['POST'])
def tutorRequestProcessing():
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    try:
        department = request.form['department']
        course = request.form['course']
    except:
        return render_template("stud_dash_req_tutor.html", username = username, feedback_return='Please select a course and department')

    requestTime = datetime.now()
    tutorAssigned = 0
    tutorName= None

    # Converting feedback_time to string
    date_time = requestTime.strftime("%m/%d/%Y, %H:%M:%S")

    setRequests(username, department, course, date_time, tutorAssigned)

    # Save feedback to a database with label as student, figure out how to access this stuff lol
    return render_template("stud_dash_req_tutor.html", username = username, feedback_return='Request sent!')

@app.route("/feedback_processing", methods=['POST'])
def feedbackProcessing():
    if isLoggedIn():
        username = " " + getCurrentUsername()
    else:
        username = ""

    feedback = request.form['feedback']
    if feedback == "":
        return render_template("stud_dash_feedback.html",feedback_return='Please provide feedback!',username=username)
    # For recording time of feedback given
    feedback_time = datetime.now()

    # Converting feedback_time to string
    date_time = feedback_time.strftime("%m/%d/%Y, %H:%M:%S")

    setFeedback(date_time, feedback, getCurrentUsername())
    app.logger.info(feedback)

    # Save feedback to a database with label as student, figure out how to access this stuff lol
    return render_template("stud_dash_feedback.html",feedback_return='Thanks for sharing your feedback!',username=username)


@app.route("/logout")
def logout():
    attemptLogout()
    return render_template("login.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loggingIn", methods=['POST'])
def loggingIn():
    if not isLoggedIn():
        username = request.form['user_input']
        password = request.form['pass_input']
        if attemptLogin(username, password):
            username = " " + username
            if getisprof() == "0":
                return render_template("stud_dash_req_tutor.html", username = username)
            else:
                return render_template("prof_dash_add_tutor.html", username = username)
        else:
            return render_template("login.html", login_failed='*Incorrect username or password.')
    else:
        return render_template("login.html", login_failed='*Already Logged In.')

@app.route("/registering", methods=['POST'])
def registering():
    if not isLoggedIn():
        email = request.form['email_reg']
        username = request.form['user_reg']
        password1 = request.form['pass1_reg']
        password2 = request.form['pass2_reg']

        if (not isEmailValid(email)):
            return render_template("login.html", register_failed='*You entered an invalid email address.')
        elif (not isUsernameValid(username)):
            return render_template("login.html", register_failed='*You entered an invalid username.')
        elif (not isPasswordValid(password1)):
            return render_template("login.html", register_failed='*You entered an invalid password.')
        elif (password1 != password2):
            return render_template("login.html", register_failed='*Passwords do not match.')
        elif (not isUsernameAvailable(username)):
            return render_template("login.html", register_failed='*Username is already taken.')
        #check email validity
        #save information

        registerNewUser(email, username, password1)
        setisprof()
        setCurrentUsername(username)
        return render_template("stud_dash_req_tutor.html")
    else:
        return render_template("login.html", register_failed='*Already Logged In.')


if __name__ == "__main__":
    app.run(debug=True)
