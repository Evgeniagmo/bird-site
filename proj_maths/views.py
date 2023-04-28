from django.shortcuts import render, redirect
from django.core.cache import cache
from . import terms_work
from . import quiz
from . models import Russianbirds
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

def show_test(request):
    return render(request, "test.html")

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

    return render(request, "quiz.html", context={"terms": quizzes[request.session.session_key].qna,
                                                 "quiz_start": True})


def check_quiz(request):
    if request.method == "POST":
        global quizzes
        for i in range(1, 5+1):  #TODO: вынести количество вопросов в .env
            quizzes[request.session.session_key]\
                .record_user_answer(request.POST.get("answer" + "-" + str(i)))
        answers = quizzes[request.session.session_key].get_user_answers()
        marks = quizzes[request.session.session_key].check_quiz()
        return render(request, "quiz.html", context={"terms": quizzes[request.session.session_key].qna,
                                                     "quiz_start": False,
                                                     "answers": answers,
                                                     "marks": marks})
    return redirect("/quiz")
