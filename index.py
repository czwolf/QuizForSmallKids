import random
from flask import Flask, render_template, request, redirect, url_for, session
import string
import os
import pandas as pd
from quiz import Quiz2 as q, Quiz, Numbers, NumbersInt, NumbersFloat, Letters, FileSystem, Storage, DataManager, Words

app = Flask(__name__)
secret_key = os.urandom(10)

app.secret_key = secret_key

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/numbers", methods=["POST", "GET"])
def numbers():
    all_answers = "answered_numbers.csv"
    template_name = "number.html"
    end = False
    answer_correct = 0
    answer_failed = 0
    percentage_correct = 0
    percentage_failed = 0
    correctness = None
    failures = []
    numbers_type = session.get("numbers_type")

    file_storage = FileSystem(all_answers)
    data_manager = DataManager(storage=file_storage)

    if request.method == "POST":
        if request.form.get("numbers_type"):
            numbers_type = request.form.get("numbers_type")
            session["numbers_type"] = numbers_type

    if request.args.get("run") == "True":
        return render_template(template_name)

    else:
        if numbers_type == "int":
            quiz_name = "Numbers_quiz_int"
            quiz_numbers = NumbersInt()
            random_number = quiz_numbers.get_random_number()
        else:
            quiz_name = "Numbers_quiz_float"
            quiz_numbers = NumbersFloat()
            random_number = quiz_numbers.get_random_number()

        if request.args.get("delFile") == "True":
            data_manager.delete()

        if os.path.exists(all_answers):
            i = quiz_numbers.set_counter(all_answers)
        else:
            i = 0

        if request.args.get("answer") == "Correct":
            correctness = True

        if request.args.get("answer") == "Fail":
            correctness = False

        if correctness is not None:
            data_manager.save_answer(correctness=correctness,
                                     answer=request.args.get("number"),
                                     quiz_name=quiz_name,
                                     i=i)

        if request.args.get("end") == "True":
            end = True
            session.pop("numbers_type")
            try:
                session.pop("random_number")
            except:
                pass

            if os.path.exists(all_answers):
                df = pd.read_csv(all_answers, sep=";", names=["quiz_name", "num", "correctness", "item"])
                num_of_questions = len(df)
                answer_correct = df["correctness"].sum()
                answer_failed = num_of_questions - answer_correct
                percentage_correct = (answer_correct / num_of_questions) * 100
                percentage_failed = (answer_failed / num_of_questions) * 100
                try:
                    failures = data_manager.get_failures_basic()
                except FileNotFoundError:
                    pass
            else:
                pass

        return render_template(template_name,
                               failures=failures,
                               number=random_number,
                               end=end,
                               answer_correct=answer_correct,
                               answer_failed=answer_failed,
                               percentage_correct=percentage_correct,
                               percentage_failed=percentage_failed)


@app.route("/letters")
def letters():
    all_answers = "answered_letters.csv"
    template_name = "letter.html"
    end = False
    answer_correct = ""
    answer_failed = ""
    percentage_correct = 0
    percentage_failed = 0
    correctness = None
    quiz_name = "Letters_quiz"
    failures = []

    storage = FileSystem(all_answers)
    data_manager = DataManager(storage=storage)


    if request.args.get("run") == "True":
        return render_template(template_name)

    else:
        quiz_letters = Letters()
        random_letter = quiz_letters.get_random_letter()

        if request.args.get("delFile") == "True":
            data_manager.delete()

        if os.path.exists(all_answers):
            i = quiz_letters.set_counter(all_answers)
        else:
            i = 0

        if request.args.get("answer") == "Correct":
            correctness = True

        if request.args.get("answer") == "Fail":
            correctness = False

        if correctness is not None:
            data_manager.save_answer(correctness=correctness,
                                     answer=request.args.get("letter"),
                                     quiz_name=quiz_name,
                                     i=i)

        if request.args.get("end") == "True":
            end = True

            if os.path.exists(all_answers):
                df = pd.read_csv(all_answers, sep=";", names=["quiz_name", "num", "correctness", "item"])
                num_of_questions = len(df)
                answer_correct = df["correctness"].sum()
                answer_failed = num_of_questions - answer_correct
                percentage_correct = (answer_correct / num_of_questions) * 100
                percentage_failed = (answer_failed / num_of_questions) * 100
                try:
                    failures = data_manager.get_failures_basic()
                except FileNotFoundError:
                    pass
            else:
                pass

        return render_template(template_name,
                               failures=failures,
                               letter=random_letter,
                               end=end,
                               answer_correct=answer_correct,
                               answer_failed=answer_failed,
                               percentage_correct=percentage_correct,
                               percentage_failed=percentage_failed)


@app.route("/words")
def words():
    words_list = [
        "Dům", "Kočka", "Pes", "Stůl", "Kresba", "Auto", "Hračka", "Jablko", "Klíč", "Kniha",
        "Hora", "Strom", "Míč", "Květina", "Okno", "Hlava", "Ruka", "Noha", "Obraz", "Kluk",
        "Holka", "Dítě", "Rybka", "Lampa", "Měsíc", "Slunce", "Zahrada", "Obloha", "Lístek",
        "Město", "Zvíře", "Loď", "Nůžky", "Škola", "Pero", "Hrad", "Růže", "Motýl", "Srdce",
        "Zmrzlina", "Koš", "Řeka", "Kolo", "Medvěd", "Zima", "Léto", "Podlaha", "Střecha",
        "Dveře", "Stín", "Chléb", "Cukr", "Hřebík", "Lžíce", "Stoleček", "Třída", "Mrak",
        "Vlak", "Ryba", "Lopatka", "Krabice", "Třešeň", "Banán", "Hříbek", "Ořech", "Záhon",
        "Králík", "Zámek", "Husa", "Krava", "Okurka", "Brambora", "Pomeranč", "Hvězda",
        "Zrcadlo", "Postýlka", "Pták", "Lev", "Sova", "Pavučina", "Zvon", "Klavír", "Přítel",
        "Zahrádka", "Košík", "Pomoc", "Zvonek", "Cihla", "Hračky", "Čepice", "Třešeň"
    ]
    # word = random.choice(names_list)

    all_answers = "answered_words.csv"
    template_name = "word.html"
    end = False
    answer_correct = ""
    answer_failed = ""
    percentage_correct = 0
    percentage_failed = 0
    correctness = None
    quiz_name = "Words_quiz"
    failures = []

    storage = FileSystem(all_answers)
    data_manager = DataManager(storage=storage)

    if request.args.get("run") == "True":
        return render_template(template_name)

    else:
        quiz_words = Words(words_list=words_list)
        random_word = quiz_words.get_random_word()

        if request.args.get("delFile") == "True":
            data_manager.delete()

        if os.path.exists(all_answers):
            i = quiz_words.set_counter(all_answers)
        else:
            i = 0

        if request.args.get("answer") == "Correct":
            correctness = True

        if request.args.get("answer") == "Fail":
            correctness = False

        if correctness is not None:
            data_manager.save_answer(correctness=correctness,
                                     answer=request.args.get("word"),
                                     quiz_name=quiz_name,
                                     i=i)

        if request.args.get("end") == "True":
            end = True

            if os.path.exists(all_answers):
                df = pd.read_csv(all_answers, sep=";", names=["quiz_name", "num", "correctness", "item"])
                num_of_questions = len(df)
                answer_correct = df["correctness"].sum()
                answer_failed = num_of_questions - answer_correct
                percentage_correct = (answer_correct / num_of_questions) * 100
                percentage_failed = (answer_failed / num_of_questions) * 100
                try:
                    failures = data_manager.get_failures_basic()
                except FileNotFoundError:
                    pass
            else:
                pass

        return render_template(template_name,
                               failures=failures,
                               word=random_word,
                               end=end,
                               answer_correct=answer_correct,
                               answer_failed=answer_failed,
                               percentage_correct=percentage_correct,
                               percentage_failed=percentage_failed)




@app.route("/questions", methods=["GET", "POST"])
def questions():
    question_set_file = "question_set_file.txt"

    if request.method == "POST" and (request.form.get("question_set")):
        q.set_selected_question_set(question_set_file, request.form.get("question_set"))

    # questions = list(question_dict.items())
    # random_key, random_value = random.choice(questions)
    temp_file = "temp.csv"
    file_name = "questions.csv"
    template_name = "question.html"

    end = False
    answer_correct = 0
    answer_failed = 0
    percentage_correct = 0
    percentage_failed = 0
    failures = []
    answer = None
    random_key = None
    random_value = None

    if os.path.exists(question_set_file):
        sett = q.get_selected_question_set(question_set_file)
        question_dict = q.get_questions_dict(sett)
        questions = list(question_dict.items())
        random_key, random_value = random.choice(questions)

    if request.args.get("run") == "True" and request.args.get("end") == "False":
        q.remove_file(temp_file)
        q.remove_file(question_set_file)

    if request.args.get("run") == "False" and request.args.get("end") != "True":
        q.set_temp(temp_file, random_key, random_value)

    if request.args.get("run") == "True":
        return render_template(template_name)
    else:
        if request.args.get("delFile") == "True":
            q.remove_file(file_name)

        if os.path.exists(file_name):
            i = q.set_counter(file_name)
        else:
            i = 0

        if request.method == "POST" and request.form.get("answer"):
            answer = request.form.get("answer")
            answer = answer.strip()
            saved_question_data = q.read_temp_file(temp_file)
            saved_random_key = saved_question_data[0]

            if answer == saved_random_key:
                q.set_correct_answer(file_name, i)
            else:
                q.set_fail_answer(file_name, i, answer)

        if request.args.get("end") == "True":
            q.remove_file(temp_file)
            end = True
            df = pd.read_csv(file_name, sep=";", names=["num", "answer", "item"], encoding="windows-1250")
            num_of_questions = len(df)
            answer_correct = df["answer"].sum()
            answer_failed = num_of_questions - answer_correct
            percentage_correct = (answer_correct / num_of_questions) * 100
            percentage_failed = (answer_failed / num_of_questions) * 100
            failures = q.failures(file_name)

        return render_template(template_name, failures=failures, random_key=random_key, end=end,
                               random_value=random_value, answer_correct=answer_correct,
                               answer_failed=answer_failed, percentage_correct=percentage_correct,
                               percentage_failed=percentage_failed)


@app.route("/state")
def state():
    return render_template("state.html")


@app.route("/city")
def city():
    return render_template("city.html")


if __name__ == '__main__':
    app.run(debug=True)