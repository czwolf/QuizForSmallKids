import random
from flask import Flask, render_template, request, redirect, url_for
import string
import os
import pandas as pd
from quiz import Quiz as q

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/numbers")
def numbers():
    file_name = "numbers.csv"
    template_name = "number.html"
    number = random.randint(1, 100)
    end = False
    answer_correct = 0
    answer_failed = 0
    percentage_correct = 0
    percentage_failed = 0
    failures = []

    if request.args.get("run") == "True":
        return render_template(template_name)
    else:
        if request.args.get("delFile") == "True":
            q.remove_file(file_name)

        if os.path.exists(file_name):
            i = q.set_counter(file_name)
        else:
            i = 0

        if request.args.get("answer") == "Correct":
            q.set_correct_answer(file_name, i)

        if request.args.get("answer") == "Fail":
            q.set_fail_answer(file_name, i, str(number))

        if request.args.get("end") == "True":
            end = True
            df = pd.read_csv(file_name, sep=";", names=["num", "answer", "item"])
            num_of_questions = len(df)
            answer_correct = df["answer"].sum()
            answer_failed = num_of_questions - answer_correct
            percentage_correct = (answer_correct / num_of_questions) * 100
            percentage_failed = (answer_failed / num_of_questions) * 100
            failures = q.failures(file_name)

        return render_template(template_name, failures=failures, number=number, end=end, answer_correct=answer_correct, answer_failed=answer_failed,percentage_correct=percentage_correct,percentage_failed=percentage_failed)

@app.route("/letters")
def letters():
    file_name = "letters.csv"
    template_name = "letter.html"
    letter = random.choice(string.ascii_uppercase)
    letter_lower = letter.lower()
    end = False
    answer_correct = 0
    answer_failed = 0
    percentage_correct = 0
    percentage_failed = 0
    failures = []

    if request.args.get("run") == "True":
        return render_template(template_name)
    else:
        if request.args.get("delFile") == "True":
            q.remove_file(file_name)

        if os.path.exists(file_name):
            i = q.set_counter(file_name)
        else:
            i = 0

        if request.args.get("answer") == "Correct":
            q.set_correct_answer(file_name, i)

        if request.args.get("answer") == "Fail":
            q.set_fail_answer(file_name, i, str(letter))

        if request.args.get("end") == "True":
            end = True
            df = pd.read_csv(file_name, sep=";", names=["num", "answer", "item"])
            num_of_questions = len(df)
            answer_correct = df["answer"].sum()
            answer_failed = num_of_questions - answer_correct
            percentage_correct = (answer_correct / num_of_questions) * 100
            percentage_failed = (answer_failed / num_of_questions) * 100
            failures = q.failures(file_name)

        return render_template(template_name, failures=failures, letter=letter,letter_lower=letter_lower, end=end,
                               answer_correct=answer_correct, answer_failed=answer_failed,
                               percentage_correct=percentage_correct, percentage_failed=percentage_failed)

@app.route("/words")
def words():
    names_list = [
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
    word = random.choice(names_list)
    return render_template("word.html",word = word)

@app.route("/state")
def state():
    return render_template("state.html")

@app.route("/city")
def city():
    return render_template("city.html")


if __name__ == '__main__':
    app.run(debug=True)