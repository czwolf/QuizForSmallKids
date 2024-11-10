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

    file_name = "words.csv"
    template_name = "word.html"
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
            q.set_fail_answer(file_name, i, str(word))

        if request.args.get("end") == "True":
            end = True
            df = pd.read_csv(file_name, sep=";", names=["num", "answer", "item"], encoding="windows-1250")
            num_of_questions = len(df)
            answer_correct = df["answer"].sum()
            answer_failed = num_of_questions - answer_correct
            percentage_correct = (answer_correct / num_of_questions) * 100
            percentage_failed = (answer_failed / num_of_questions) * 100
            failures = q.failures(file_name)

        return render_template(template_name, failures=failures, word=word, letter_lower=letter_lower, end=end,
                               answer_correct=answer_correct, answer_failed=answer_failed,
                               percentage_correct=percentage_correct, percentage_failed=percentage_failed)

@app.route("/questions", methods=["GET", "POST"])
def questions():
    question_dict = {
        "slunce": "Co svítí na obloze a dává nám teplo? Nápověda: Je žluté a vidíme ho hlavně přes den.",
        "měsíc": "Co svítí na obloze v noci a mění svůj tvar? Nápověda: Je kulatý a září, když je tma.",
        "auto": "Co jezdí po silnici a má čtyři kola? Nápověda: Může být malé nebo velké, obvykle má volant.",
        "tráva": "Co je zelené a roste na zemi? Nápověda: Sekáme to sekačkou na zahradě.",
        "ryba": "Jaké zvíře žije ve vodě a má ploutve? Nápověda: Je tichá a plave v jezerech nebo moři.",
        "kočka": "Jaké zvíře má rádo mléko a vrní, když je spokojené? Nápověda: Ráda loví myši.",
        "pes": "Jaké zvíře štěká a rádo běhá za míčkem? Nápověda: Často je nejlepším přítelem člověka.",
        "pták": "Co létá na obloze a má peří? Nápověda: Některé druhy si staví hnízdo.",
        "mrak": "Co je na obloze, když se schyluje k dešti? Nápověda: Může být bílý nebo šedý.",
        "mléko": "Co pijí děti, aby měly silné kosti? Nápověda: Vyrábí se z něj sýr a jogurt.",
        "kolo": "Na čem můžeme jezdit, když to má dvě kola a pedály? Nápověda: Děti se na tom učí rovnováhu.",
        "včela": "Jaký hmyz vyrábí med? Nápověda: Má žluto-černé pruhy a bzučí.",
        "zebra": "Jaké zvíře je pruhované a podobá se koni? Nápověda: Najdeme ji v Africe nebo v zoo.",
        "čokoláda": "Jaká sladkost je hnědá a vyrábí se z kakaa? Nápověda: Často se dává jako dárek na Vánoce.",
        "kouzelník": "Kdo dokáže předvádět triky a iluze, aby překvapil lidi? Nápověda: Nosí často klobouk a hůlku.",
        "zima": "Jaké roční období je, když sněží a mrzne? Nápověda: Nosíme teplé oblečení a jsou Vánoce.",
        "prst": "Co máš na ruce pětkrát? Nápověda: Pomáhá ti chytat věci.",
        "zmrzlina": "Jaká sladkost je studená a jíme ji hlavně v létě? Nápověda: Může být vanilková nebo čokoládová.",
        "želva": "Jaké zvíře má krunýř a pohybuje se velmi pomalu? Nápověda: Žije dlouho a umí plavat.",
        "hřib": "Jakou rostlinu sbíráme v lese a dáváme ji do polévky? Nápověda: Je to houba s kloboukem.",
        "letadlo": "Co létá na nebi a přepravuje lidi na dlouhé vzdálenosti? Nápověda: Má křídla a motory.",
        "jablko": "Jaké ovoce je kulaté, červené nebo zelené a roste na stromě? Nápověda: Známe ho jako symbol zdraví.",
        "šnek": "Jaký tvor má ulitu na zádech a pohybuje se velmi pomalu? Nápověda: Nechává za sebou slizkou stopu.",
        "zrcadlo": "Na co se díváme, když chceme vidět svůj odraz? Nápověda: Najdeme ho v koupelně.",
        "hory": "Kde je sníh i v létě, a lidé tam jezdí lyžovat? Nápověda: Jsou vysoké a krásné.",
        "kamarád": "Jak nazýváme člověka, se kterým se rádi smějeme a hrajeme? Nápověda: Může to být spolužák nebo soused.",
        "moře": "Kde je hodně vody, písek na pláži a lidé se tam koupou? Nápověda: Má slanou vodu.",
        "králík": "Jaké zvíře má dlouhé uši a rádo chroupá mrkev? Nápověda: Žije v norách.",
        "myš": "Jaký malý hlodavec má rád sýr a může žít v domě? Nápověda: Kočka ho často loví.",
        "svíčka": "Co zapalujeme na dortu při oslavě narozenin? Nápověda: Hoří a dělá plamínek.",
        "strom": "Co má kmen, větve a listy, a roste v lese? Nápověda: Dává nám kyslík.",
        "klavír": "Na jaký hudební nástroj se hraje prsty a má černé a bílé klávesy? Nápověda: Velmi krásně zní.",
        "vlak": "Co jezdí po kolejích a vozí lidi nebo náklad? Nápověda: Má mnoho vagónů.",
        "knížka": "Co čteme, abychom se dozvěděli příběhy nebo naučili něco nového? Nápověda: Má stránky a může být tlustá nebo tenká.",
        "zvon": "Co vydává hlasitý zvuk, když ho rozkýváme? Nápověda: Najdeme ho v kostele.",
        "šachy": "Jaká hra se hraje na černobílé šachovnici s figurkami? Nápověda: Cílem je dostat krále soupeře.",
        "balón": "Co se nafukuje a létá, když ho pustíme? Nápověda: Je barevný a děti si s ním hrají.",
        "mráz": "Co způsobuje, že voda venku zmrzne a stromy jsou bílé? Nápověda: Je velmi studený a je v zimě.",
        "kostka": "Jaký předmět má šest stěn a často ho používáme ve hrách? Nápověda: Na každé straně jsou tečky.",
        "pohádka": "Jaký druh příběhu má často princezny, čaroděje a kouzel? Nápověda: Čteme ji dětem na dobrou noc.",
        "popelka": "Která pohádková postava ztratila střevíček na bále? Nápověda: Její jméno je od slova 'popel'.",
        "jízdní řád": "Jak se nazývá seznam časů, kdy přijíždí autobusy nebo vlaky? Nápověda: Najdeme ho na zastávkách.",
        "polévka": "Jak se říká jídlu, které jíme lžící a bývá teplé? Nápověda: Obvykle se podává v talíři nebo misce.",
        "čáp": "Jaký pták má dlouhé nohy a nosí miminka podle pověsti? Nápověda: Najdeme ho u rybníků.",
        "švestka": "Jaké ovoce je tmavě modré a často se z něj dělají knedlíky? Nápověda: Roste na stromě a je sladké.",
        "saně": "Na čem děti jezdí v zimě z kopce dolů? Nápověda: Potřebují k tomu sníh.",
        "kačer": "Jaký vodní pták má oranžový zobák a rád plave? Nápověda: Říká 'kvák kvák'.",
        "perník": "Jaká sladkost je kořeněná a peče se hlavně na Vánoce? Nápověda: Může mít různé tvary, třeba srdíčko.",
        "dýně": "Jaká zelenina je oranžová, kulatá a často se vyřezává na Halloween? Nápověda: Je velká a dužnatá.",
        "vítr": "Co vane venku a rozhýbává listy stromů? Nápověda: Cítíme ho, ale nevidíme."
    }
    # question_dict = {"koza":"zvíře", "praha":"město"}

    questions = list(question_dict.items())
    random_key, random_value = random.choice(questions)
    file_name = "questions.csv"
    template_name = "question.html"
    end = False
    answer_correct = 0
    answer_failed = 0
    percentage_correct = 0
    percentage_failed = 0
    failures = []
    answer = None

    if request.args.get("run") == "True":
        return render_template(template_name)
    else:
        if request.args.get("delFile") == "True":
            q.remove_file(file_name)

        if os.path.exists(file_name):
            i = q.set_counter(file_name)
        else:
            i = 0

        if request.method == "POST":
            answer = request.form.get("answer")
            print(answer, random_key)
            if answer == random_key:
                q.set_correct_answer(file_name, i)
            else:
                q.set_fail_answer(file_name, i, answer)

        if request.args.get("end") == "True":
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