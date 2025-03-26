from controller.database import db
import enum
from datetime import datetime
from sqlalchemy import Integer, Enum


class QualificationEnum(enum.Enum):
    Foundation= "foundation"
    Diploma_DS = "diploma_ds"
    Diploma_Prog = "diploma_programming"
    BSc = "bsc"
    BS = "bs"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date)  # Date of Birth field
    class_ = db.Column(db.Enum(QualificationEnum), nullable=True)
    roles = db.relationship('Role', secondary='user_role')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

class UserRole(db.Model):
    __tablename__ = "user_role"
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'),nullable= False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),nullable= False)

class Lebel:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_ = db.Column(db.Enum(QualificationEnum), nullable=False)

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    class_ = db.Column(db.Enum(QualificationEnum), nullable=False)

    # Define explicit relationship without backref in Quiz
    quizzes = db.relationship("Quiz", 
                              back_populates="subject", 
                              cascade="all, delete-orphan", 
                              passive_deletes=True)

class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete="CASCADE"), nullable=False)
    module = db.Column(db.String(100), nullable=False)

    # Define explicit relationship to Subject
    subject = db.relationship("Subject", back_populates="quizzes")  

    # Ensure Questions are deleted when Quiz is deleted
    questions = db.relationship("Question", cascade="all, delete-orphan", passive_deletes=True)


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete="CASCADE"), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

    quiz = db.relationship("Quiz", back_populates="questions")  
#class QuizQuestion(db.Model):
#    __tablename__ = "quiz_question"
#    id = db.Column(db.Integer, primary_key=True)
#    quiz_id= db.Column(db.Integer, db.ForeignKey('quiz.id'),nullable= False)
#    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),nullable= False)

#class Option(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    description = db.Column(db.String(1000), nullable=False)
#    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),nullable= False)

#class QuestionOption(db.Model):
#    __tablename__ = "question_option"
#    id = db.Column(db.Integer, primary_key=True)
#    question_id= db.Column(db.Integer, db.ForeignKey("question.id"),nullable= False)
#    option_id = db.Column(db.Integer, db.ForeignKey('option.id'),nullable= False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer,nullable=False)
    submission_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("scores", cascade="all, delete-orphan", passive_deletes=True))
    quiz = db.relationship("Quiz", backref=db.backref("scores", cascade="all, delete-orphan", passive_deletes=True))