import re

from sklearn.metrics import top_k_accuracy_score
from . import db
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
import json
from .models import AskedQuestion, User
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        id = request.form.get("idddd")
        answer = request.form.get('textarea')
        question = AskedQuestion.query.filter_by(
            id=id).first()
        question.answer = answer
        db.session.commit()

    if current_user.is_authenticated:
        first_names = []
        all_questions = AskedQuestion.query.order_by(AskedQuestion.date)
        print(type(all_questions))
        all_questions_list = all_questions[:]
        all_questions_list.reverse()

        print(len(all_questions_list))
        questions = []
        for question in all_questions_list:
            questions.append(question)
            first_names.append(User.query.filter_by(
                id=question.user_id).first())
        print(len(questions))

        return render_template("home.html", user=current_user, all_questions=questions, first_names=first_names)
    else:
        return redirect(url_for("auth.login"))


@views.route('/ask', methods=['GET', 'POST'])
def ask():
    global current_url
    current_url = url_for("views.ask")
    if request.method == 'POST':
        subject = request.form.get("subject")
        body = request.form.get("body")
        img1 = request.form.get("image1")

        img2 = request.form.get("image2")
        img3 = request.form.get("image3")
        img_list = [img1, img2, img3]
        for counter in img_list:
            if type(counter) == None:
                counter = ""

        if current_user.is_authenticated == False:
            flash("Please login before submitting a question.", category="error")

        elif len(subject) < 2:
            flash("Please enter a proper subject.", category="error")

        elif len(body) < 5:
            flash(
                "The body does not have enough characters. Please add more.", category="error")
        else:
            for counter in img_list:
                if counter == "":
                    counter = None

            new_question = AskedQuestion(
                subject=subject, answer="", body=body, image1=img1, image2=img2, image3=img3, user_id=current_user.id)
            db.session.add(new_question)
            db.session.commit()
            flash('Question posted!', category="success")
            for counter in img_list:
                if counter == None:
                    counter = ""

            return(redirect(url_for("views.home")))
    return render_template('ask.html', user=current_user)


@views.route('/contact', methods=['GET', 'POST'])
def contact():
    global current_url
    current_url = url_for("views.contact")
    if request.method == 'POST':
        if not current_user.is_authenticated:
            email = request.form.get('email')
        if current_user.is_authenticated:
            email = current_user.email
        subject = request.form.get("subject")
        body = request.form.get('body')
        file = open('messages.txt', 'a')
        file.write(
            f"\n\n----------\nBy: {email}\nSubject: {subject}\nMessage: {body}\n----------")
        if current_user.is_authenticated:
            return redirect(url_for("views.home"))
        else:
            return redirect(url_for("auth.login"))

    return render_template('contact.html', user=current_user)
