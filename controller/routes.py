from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from controller.model import * 
from werkzeug.security import *
from datetime import datetime
from collections import Counter
import matplotlib
matplotlib.use('Agg')  # ✅ Use a non-GUI backend

from matplotlib import pyplot as plt 
import os
from flask import send_file


@app.route('/')
def home():
    return render_template('home2.html')
@app.route('/admin_')
def admin_dashboard():
    users = User.query.all()
    total_users = len(users) - 1 
    subjects=Subject.query.all() 
    quizzes = Quiz.query.all() 
    return render_template('admin_dash.html', users=users,total_users=total_users,subjects=subjects,active_page="home",quizzes=quizzes)

@app.route('/remove_sub', methods=['GET', 'POST'])
def remove_sub():
    if request.method == 'POST':
        subject = request.form.get('subject_id')
        subject_db = Subject.query.filter_by(id=subject).first()  # Find subject by name
        if subject_db:
            db.session.delete(subject_db)
        db.session.commit()
        flash("successfully deleted.")
        return redirect(url_for('subject_dashboard'))

    if request.method == 'GET':
        
        return redirect(url_for('subject_dashboard'))

@app.route('/add_sub', methods=['GET', 'POST'])
def add_sub():
    if request.method == 'POST':
        subject = request.form.get('subject_name')
        department = request.form.get('department')
        level = request.form.get('level')
        new_sub = Subject(
            name = subject,
            class_= QualificationEnum[level] if level in QualificationEnum.__members__  else QualificationEnum['Foundation'],
            department = department
            #email = 'admin@gmail.com',
            #password= generate_password_hash('2003'),
            #class_=QualificationEnum("Class 8"),
            #roles = [admin_role]
        )
        db.session.add(new_sub)   
        db.session.commit()
        flash("successfully added a new subject.")
        return redirect(url_for('subject_dashboard'))

    if request.method == 'GET':
        return render_template('add_sub.html')


@app.route('/user_')
def user_dashboard():
    user = User.query.filter_by(id=session.get('user_id')).first()
    if not user:
        flash("User not logged in.")
        return redirect(url_for('login'))
    subjects= Subject.query.filter_by(class_=user.class_).all()
    quizzes = Quiz.query.all()
    return render_template('user_dash.html',page_name="Dashboard",user =user,subjects = subjects,quizzes = quizzes)

@app.route('/user/quiz')
def user_quiz_dashboard():
    user = User.query.filter_by(id=session.get('user_id')).first()
    quizzes = Quiz.query.all()
    subject=Subject.query.all()
    default_search_input = request.args.get('search', '')
    if request.method == 'GET':
        return render_template('quiz_access.html',page_name="Quiz",quizzes = quizzes,subjects=subject,default_search_input=default_search_input, user=user)
    return None


@app.route('/user/profile')
def profile():
    user_id = session.get('user_id')
    if(user_id):
        user = User.query.filter_by(id=user_id).first()
        return render_template('profile.html',user=user, page_name="Profile")
    else:
        return redirect(url_for('logout'))


#@app.route('/user/quiz/attent')
#def attend_quiz():
#    quizzes = Quiz.query.all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('userName')  # Get email from form
        password = request.form.get('password')  # Get password from form
        
        user = User.query.filter_by(email = email).first()
        if not user:
            flash("User Not Found", "danger")
            return redirect(url_for('login'))
        if not check_password_hash(user.password,password):
            
            flash("Invalid credentials, please try again.", "danger")
            return redirect(url_for('login'))
        else:
            is_admin = any(role.name == "admin" for role in user.roles)
            session["user_id"] = user.id
            session["is_admin"] = is_admin
            session["username"] = user.name
            flash("Login successful!", "success")
            if is_admin:
                return redirect(url_for('admin_dashboard'))  # Redirect to Admin Panel
            else:
                return redirect(url_for('user_dashboard'))  # Redirect to User Home
        
    return render_template('login.html' , page_name="login")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')  # Get email from form
        user = User.query.filter_by(email = email).first()
        
        if not user:
            password = request.form.get('password')  # Get password from form
            name = request.form.get('name')
            dob = datetime.strptime(request.form.get('dob'), "%Y-%m-%d").date()
            class_value = request.form.get('level')
            #class_ = request.form.get('class')
            hashed_password = generate_password_hash(password)

            user_role = Role.query.filter_by(name='user').first()
            if not user_role:
                flash("User role not found. Please contact support.", "danger")
                return redirect(url_for('register'))
            # Create a new user instance with default role 'user'
            new_user = User(name=name, email=email, dob=dob, class_= QualificationEnum[class_value] if class_value in QualificationEnum.__members__  else QualificationEnum['Foundation'] , password=hashed_password, roles=[user_role])

            # Add and commit the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        else: 
            flash("Email in use already", "danger")
            return redirect(url_for('login'))
        
    return render_template('signup.html',page_name="signup")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("Successfully Logged Out", "success")
    return render_template('login.html',page_name="login")

@app.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == 'GET':
        email=request.args.get('email')
        if email:
            return render_template('reset.html', page_name="reset",email=email)
        else:
            return render_template('reset.html', page_name="reset",email="")
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email = email).first()
        if user:
            dob = datetime.strptime(request.form.get('dob'), "%Y-%m-%d").date()
            if dob == user.dob:
                password = request.form.get('password')  # Get password from form
                hashed_password = generate_password_hash(password)
                user.password = hashed_password
                db.session.commit()  # Save changes to the database
                flash("Password reset successful.", "success")
                return redirect(url_for('logout'))
            else: 
                flash("Date of Birth does not match.", "danger")
                return redirect(url_for('forget'))
        else:
            flash("No user exist for the email provided.", "danger")
            return redirect(url_for('logout'))

    return render_template('reset.html', page_name="reset")

@app.route('/subject_dash')
def subject_dashboard():
    if request.method == 'GET':
        role = session.get('is_admin')
        if role:
            subjects=Subject.query.all() 
            return render_template('subject_dash.html',subjects=subjects,active_page="subjects")
        else:
            return redirect(url_for('login'))

@app.route('/quiz_dash')
def quiz_dashboard():
    if request.method == 'GET':
        role = session.get('is_admin')
        if role:
            quiz=Quiz.query.all() 
            subjects=Subject.query.all() 
            questions = Question.query.all()
            return render_template('quiz_das.html',subjects=subjects, quiz=quiz,questions=questions, active_page="quiz")
        else:
            return redirect(url_for('login'))

@app.route('/quiz_dash/del_quiz',methods=['POST','GET'])
def del_quiz():
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        quiz_db = Quiz.query.filter_by(id=quiz_id).first()  # Find subject by name
        if quiz_db:
            db.session.delete(quiz_db)
        db.session.commit()
        return redirect(url_for('quiz_dashboard'))
    return None

@app.route('/quiz_dash/add_quiz',methods=['POST','GET'])
def add_quiz():
    quiz=Quiz.query.all() 
    subjects=Subject.query.all() 
    if request.method == 'POST':
        subject = request.form.get('subject_name')
        module = request.form.get('module')
        subjects = Subject.query.filter_by(name=subject).first()
        new_q = Quiz(
            subject_id = subjects.id,
            #class_= QualificationEnum[level] if level in QualificationEnum.__members__  else QualificationEnum['Foundation'],
            module = module
            #email = 'admin@gmail.com',
            #password= generate_password_hash('2003'),
            #class_=QualificationEnum("Class 8"),
            #roles = [admin_role]
        )
        db.session.add(new_q)   
        db.session.commit()
        quiz_id = new_q.id
        #flash("successfully added a new Quiz.")
        return redirect(url_for('add_questions',quiz_id=quiz_id))
    if request.method == 'GET':
        subject_names = [getattr(sub, 'name') for sub in subjects]
        return render_template('quiz_add.html',subject_names=subject_names)

@app.route('/question_delete',methods=['GET','POST'])
def del_question():
    if request.method == 'POST':
        question_id = request.form.get("question_id")
        question_db = Question.query.filter_by(id=question_id).first()  # Find subject by name
        if question_db:
            db.session.delete(question_db)
        db.session.commit()
        return redirect(url_for('quiz_dashboard'))


@app.route('/stat',methods=['GET','POST'])
def admin_statistics_dashboard():
    if request.method == 'GET':
        scores = Score.query.all()
        quizzes = Quiz.query.all()
        subjects = Subject.query.all()
        user= User.query.all()
        class_counts = Counter([us.class_.value for us in user if us.class_ is not None])
        print(class_counts)
        labels = list(class_counts.keys())  # Class names
        values = list(class_counts.values())  # Count of students per class
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
        plt.title("User Distribution by Class")

        # Save Pie Chart Image
        pie_chart_path = os.path.join("static", "charts", "pie_chart.png")
        os.makedirs(os.path.dirname(pie_chart_path), exist_ok=True)
        plt.savefig(pie_chart_path)
        plt.close()

        # Create Bar Graph
        plt.figure(figsize=(8, 6))
        plt.bar(labels, values, color=plt.cm.Paired.colors[:len(labels)])
        plt.xlabel("Class")
        plt.ylabel("Number of Students")
        plt.title("User Distribution by Class (Bar Graph)")
        plt.xticks(rotation=15)  # Rotate x-axis labels for better visibility

        # Save Bar Chart Image
        bar_chart_path = os.path.join("static", "charts", "bar_chart.png")
        plt.savefig(bar_chart_path)
        plt.close()

        user_quiz_counts = {us.id: 0 for us in user}
        for score in scores:
            user_quiz_counts[score.user_id] += 1
        return render_template('stat_admin.html',active_page="stats",scores=scores,quizzes=quizzes,subjects=subjects,users = user,labels=labels, values=values,user_quiz_counts=user_quiz_counts)

    

@app.route('/question_details',methods=['GET','POST'])
def info_questions():
    if request.method == 'POST':
        quiz_id = request.form.get("quiz_id")
        questions = Question.query.filter_by(quiz_id=quiz_id).all() 
        return render_template('questions_info.html',questions=questions, quiz_id=quiz_id)


@app.route('/question',methods=['GET','POST'])
def add_questions():
    quiz_id = request.args.get("quiz_id")
    if request.method == 'GET':
        return render_template('add_questions.html',quiz_id=quiz_id)
    if request.method == 'POST':
        quiz_id = request.form.get("quiz_id")
        question_texts = request.form.getlist("question_text[]")
        option1s = request.form.getlist("option1[]")
        option2s = request.form.getlist("option2[]")
        option3s = request.form.getlist("option3[]")
        option4s = request.form.getlist("option4[]")
        correct_options = request.form.getlist("correct_option[]")

        for i in range(len(question_texts)):
            question = Question(
                quiz_id=quiz_id,
                text=question_texts[i],
                option1=option1s[i],
                option2=option2s[i],
                option3=option3s[i],
                option4=option4s[i],
                correct_option=int(correct_options[i])
            )
            db.session.add(question)
        
        db.session.commit()
        return redirect(url_for('quiz_dashboard'))
    return redirect(url_for('admin_dashboard'))


@app.route('/remove_user',methods=['POST'])
def rem_user():
    if request.method == 'POST':
        user = request.form.get('user_id')
        user_db = User.query.filter_by(id=user).first()  # Find subject by name
        if user_db:
            db.session.delete(user_db)
        db.session.commit()
        flash("successfully deleted.")
        return redirect(url_for('admin_dashboard'))

    if request.method == 'GET':
        return redirect(url_for('admin_dashboard'))
    return None

@app.route('/quiz_question',methods=['GET','POST'])
def quiz_question():
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        quiz_details = Quiz.query.filter_by(id=quiz_id).first()
        question_details = Question.query.filter_by(quiz_id=quiz_id).all()
        flash("After 4 Minutes the answers will be automatically submitted.")
        return render_template('attend_quiz.html', quiz_details=quiz_details, question_details=question_details)
    

@app.route('/score',methods=['Get','POST'])
def check_scoore():
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        sc = 0
        ques_count = 0
        Questions = Question.query.filter_by(quiz_id = quiz_id).all()
        for ques in Questions:
            option_chosen = request.form.get(f'question_{ques.id}')
            #print(option_chosen)
            #print(type(option_chosen))
            #print(ques.correct_option)
            #print(type(ques.correct_option))
            if (option_chosen):
                if int(option_chosen) == ques.correct_option:
                    sc = sc + 1 
                #print("1_____",sc)
            ques_count = ques_count + 1
            #print(ques_count)
        entry = Score(
            user_id = session.get('user_id'),
            quiz_id = quiz_id,
            score = (sc/ques_count)*100,
            submission_time = datetime.now()
        )
        db.session.add(entry)   
        db.session.commit()
        score , subject, quiz = returning_stuff(session.get('user_id'))
        return render_template('performence.html',page_name="performence",score=score, subject=subject,quiz=quiz )
    if request.method == 'GET':
        score , subject, quiz = returning_stuff(session.get('user_id'))
        return render_template('performence.html',page_name="performence",score=score, subject=subject,quiz=quiz)
    return None

def returning_stuff(user_id):
    scoore_entry=Score.query.filter_by(user_id=user_id).all()
    subject = Subject.query.all()
    quiz = Quiz.query.all()

    return scoore_entry, subject, quiz