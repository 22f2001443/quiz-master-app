
# Quiz Master V1

**Author:**  
Samyabrata Roy  
22f2001443  
[22f2001443@ds.study.iitm.ac.in](mailto:22f2001443@ds.study.iitm.ac.in)

---

## 🎓 Academic Background

I am pursuing a **BS in Data Science from IIT Madras** and a **BSc in Statistics from Sister Nivedita University**, along with a **Diploma in Web Development from CITC Chandigarh**.

I have a strong interest in **Non-Parametric Statistical Inference** and **Machine Learning** and truly enjoyed the journey of developing the WebApp for this project.

---

## 📌 Project Description

In this project, I developed a **multi-user quiz application** using Flask, Jinja2, SQLite, and Bootstrap.

- **Admin (Quiz Master)** manages users, subjects, chapters, and quizzes.
- **Users** can attempt quizzes and view their scores.
- Supports **CRUD operations**, **authentication**, **quiz management**, and **data visualization**.

---

## 🛠 Technologies Used

- **Flask** – Web framework (routing, templates, sessions, flash messages).
- **Flask-SQLAlchemy** – Database ORM.
- **Session** – Stores user login data securely.
- **HTML5, CSS** – Frontend structure and styling.
- **JavaScript** – Enables client-side search.
- **Werkzeug Security** – Password hashing & verification.
- **Datetime** – Quiz timestamps.
- **Collections.Counter** – Score tracking.
- **Matplotlib** – Visualizing quiz results.

---

## 🧱 DB Schema Design

### Entities and Relationships:

1. **User Table**  
   - One-to-Many with Score  
   - Many-to-Many with Role

2. **Role Table**  
   - Many-to-Many with User

3. **UserRole Table**  
   - Many-to-Many bridge for User and Role

4. **Subject Table**  
   - One-to-Many with Chapter

5. **Chapter Table**  
   - One-to-Many with Quiz  
   - Many-to-One with Subject

6. **Quiz Table**  
   - One-to-Many with Question & Score  
   - Many-to-One with Chapter

7. **Question Table**  
   - Many-to-One with Quiz

8. **Score Table**  
   - Many-to-One with User and Quiz

### Key Constraints:

- **User & Role**: Many-to-Many  
- **User & Score**: One-to-Many  
- **Subject & Chapter**: One-to-Many  
- **Chapter & Quiz**: One-to-Many  
- **Quiz & Question**: One-to-Many  
- **Quiz & Score**: One-to-Many

### 🔄 Cascade Behavior:

- Deleting a user deletes their scores.  
- Deleting a quiz deletes its questions and scores.  
- Deleting a chapter deletes its quizzes.

---

## 🏗 Architecture and Features

### Project Structure

- **controller/**: `config.py`, `database.py`, `model.py`, `route.py`
- **instance/**: database file
- **html_temps/**: Jinja templates
- **static/**
  - **CSS/**: styles
  - **Img/**: images
- **app.py**: app initializer
- **project report**: PDF

### Admin Panel Features

- Manage Subjects, Chapters, Quizzes
- Add/Edit/Delete Questions and Options
- Set correct answers and scoring rules

### User Panel Features

- Browse subjects
- Attempt quizzes
- Track scores

---

## 🚀 Flask Controllers Used

```python
@app.route('/admin_')
@app.route('/remove_sub', methods=['GET', 'POST'])
@app.route('/add_sub', methods=['GET', 'POST'])
@app.route('/user_')
@app.route('/user/quiz')
@app.route('/user/profile')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
@app.route('/logout', methods=['GET', 'POST'])
@app.route('/forget', methods=['GET', 'POST'])
@app.route('/subject_dash')
@app.route('/quiz_dash')
@app.route('/quiz_dash/del_quiz', methods=['GET', 'POST'])
@app.route('/quiz_dash/add_quiz', methods=['GET', 'POST'])
@app.route('/question_delete', methods=['GET', 'POST'])
@app.route('/stat', methods=['GET', 'POST'])
@app.route('/question_details', methods=['GET', 'POST'])
@app.route('/question', methods=['GET', 'POST'])
@app.route('/remove_user', methods=['POST'])
@app.route('/quiz_question', methods=['GET', 'POST'])
@app.route('/score', methods=['GET', 'POST'])
@app.route('/chapter_dash')
@app.route('/add_chapter', methods=['GET', 'POST'])
@app.route('/remove_chap', methods=['GET', 'POST'])
@app.route('/edit', methods=['GET', 'POST'])
