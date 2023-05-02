import os
from django.shortcuts import render, redirect
from django.core.cache import cache
from . import quiz
from .models import Russianbirds
from . import birds_db


def index(request):
    return render(request, "index.html")


def birds_list(request):
    birds = birds_db.db_get_birds_for_table()
    return render(request, "birds_list.html", context={"birds": birds})


def add_bird(request):
    return render(request, "bird_add.html")


def send_bird(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        user_email = request.POST.get("email")
        new_bird = request.POST.get("new_bird", "").lower()
        new_location = request.POST.get("new_location", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_location) == 0:
            context["success"] = False
            context["comment"] = "Локация должна быть указана"
        elif len(new_bird) == 0:
            context["success"] = False
            context["comment"] = "Птычка должна быть указана"
        elif Russianbirds.objects.filter(species_name__exact=new_bird).count() == 0:
            context["success"] = False
            context["comment"] = "Такой птычки нет("
        else:
            context["success"] = True
            context["comment"] = "Ваше наблюдение зафиксировано"
            birds_db.db_add_observation(new_bird, new_location, user_name, user_email)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "bird_request.html", context)
    else:
        add_bird(request)


def show_stats(request):
    stats = birds_db.db_get_birds_stats()
    return render(request, "stats.html", stats)


"""Глобальная переменная, в которой хранится словарь:
ключи -- ключи сессий, значения -- объекты Quiz."""
global quizzes


def start_quiz(request):
    if not request.session.session_key:
        request.session.create()

    global quizzes
    if 'quizzes' in globals():
        quizzes[request.session.session_key] = quiz.Quiz()
    else:
        quizzes = dict()
        quizzes[request.session.session_key] = quiz.Quiz()

    return render(request, "quiz.html", context={"birds": quizzes[request.session.session_key].qna,
                                                 "quiz_start": True})


def check_quiz(request):
    if request.method == "POST":
        global quizzes
        q_number = int(os.getenv("QUIZ_Q_NUMBER"))
        for i in range(1, q_number + 1):
            quizzes[request.session.session_key] \
                .record_user_answer(request.POST.get("answer" + "-" + str(i)))
        answers = quizzes[request.session.session_key].get_user_answers()
        marks = quizzes[request.session.session_key].check_quiz()
        answers_count = [atf for atf in marks if atf == True]
        mark = len(answers_count)
        mark_str = ""
        if 0 <= mark / q_number < 0.33333:
            mark_str = "Так себе("
        elif 0.33333 <= mark / q_number < 0.66667:
            mark_str = "Неплохо"
        elif 0.66667 <= mark / q_number < 1:
            mark_str = "Класс!"
        else:
            mark_str = "Превосходно!"
        return render(request, "quiz.html", context={"birds": quizzes[request.session.session_key].qna,
                                                     "quiz_start": False,
                                                     "answers": answers,
                                                     "marks": marks,
                                                     "mark": mark,
                                                     "q_number": q_number,
                                                     "mark_str": mark_str})
    return redirect("/quiz")


def get_info(request):
    return render(request, "get_info.html")


def show_info(request):
    if request.method == "POST":
        cache.clear()
        bird_name = request.POST.get("bird", "").lower()
        context = {"bird_species": bird_name}
        bird_info = {}
        if len(bird_name) == 0:
            context["success"] = False
            context["comment"] = "Птычка должна быть указана"
        elif Russianbirds.objects.filter(species_name__exact=bird_name).count() == 0:
            context["success"] = False
            context["comment"] = "Такой птычки нет("
        else:
            context["success"] = True
            context["comment"] = "Такая птычка найдена"
            bird_info = birds_db.db_get_description(bird_name)
        if context["success"]:
            context["success-title"] = ""
        for k, v in bird_info.items():
            context[k] = v
        return render(request, "show_info.html", context)
    else:
        get_info(request)
