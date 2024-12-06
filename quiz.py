import os
import random
import pandas as pd
import string
from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def save_answer(self, correctness, answer, quiz_name, i):
        pass

    @abstractmethod
    def get_failures_basic(self):
        pass

    @abstractmethod
    def delete(self):
        pass
    
class FileSystem(Storage):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_answer(self, correctness: bool, answer: str = None, quiz_name: str = None, i: int = None):
        correctness = 1 if correctness else 0

        try:
            with open(self.file_path, "a+") as file:
                if not i:
                    file.write(f"{quiz_name};1;{correctness};{answer}\n")
                else:
                    file.write(f"{quiz_name};{int(i) + 1};{correctness};{answer}\n")
        except FileNotFoundError:
            print(f"{self.file_path} not found!")

    def get_failures_basic(self):
        try:
            df = pd.read_csv(self.file_path, sep=";", names=["quiz_name", "num", "correctness", "item"])
            failures = df.loc[df["correctness"] == 0]
            return failures["item"].to_list()

        except FileNotFoundError:
            print(f"{self.file_path} not found!")

    def delete(self):
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            print(f"{self.file_path} not found!")
            

class DataManager(Storage):
    def __init__(self, storage: Storage):
        self.storage = storage

    def save_answer(self, correctness: bool, answer: str = None, quiz_name: str = None, i: int = None):
        """
        Save data to the storage.

        :param quiz_name: name of the quiz
        :param answer: Users answer
        :param i: index (number) of question
        :param correctness: True or False
        """
        return self.storage.save_answer(correctness, answer, quiz_name, i)

    def get_failures_basic(self):
        return self.storage.get_failures_basic()

    def delete(self):
        return self.storage.delete()

class Quiz:
    """
    Base class for all Quiz.
    """

    def __init__(self, name: str, file_path: str, number_of_questions: int = None, difficult: int = 1):
        self.name = name
        self.file_path = file_path
        self.number_of_questions = number_of_questions
        self.difficult = difficult

    def remove_file(self, file_path):
        try:
            os.remove(file_path)
        except FileNotFoundError:
            print(f"{file_path} not found!")

    def set_counter(self, file_path: str):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                return len(lines)
        except FileNotFoundError:
            print(f"{file_path} not found!")

    def set_correct_answer(self, file_path: str, i: str):
        try:
            with open(file_path, "a+") as file:
                if not i:
                    file.write("1;1;X\n")
                else:
                    file.write(f"{int(i) + 1};1;X\n")
        except FileNotFoundError:
            print(f"{file_path} not found!")

    def set_wrong_answer(self, file_path: str, i: str, answer: str):
        try:
            with open(file_path, "a+") as file:
                if not i:
                    file.write(f"1;0;{answer}\n")
                else:
                    file.write(f"{int(i) + 1};0;{answer}\n")
        except FileNotFoundError:
            print(f"{file_path} not found!")

    @abstractmethod
    def get_failures(self, file_path: str):
        pass

    def __repr__(self):
        return (
            f"name = {self.name}, file_path = {self.file_path}, number_of_questions = {self.number_of_questions}, difficult = {self.difficult}")


class Numbers(Quiz, ABC):
    """
    Quiz numbers
    :param number_type: int, float
    """

    def __init__(self, name, number_of_questions: int = None, range_numbers: int = 100):
        super().__init__(name, number_of_questions)
        self.range_numbers = range_numbers

    def save_wrong_answer_number(self, filename: str, number: str):
        try:
            file = open(filename, "a+")
            file.write(str(number) + "\n")
        except FileNotFoundError:
            print(f"{filename} not found!")

    def get_failures(self, file_path: str):
        try:
            with open(file_path, "r") as file:
                data = file.readlines()
                data_cleared = [item.strip() for item in data]
                return data_cleared
        except FileNotFoundError:
            print(f"{file_path} not found!")

    def __repr__(self):
        return (
            f"name = {self.name}, number_of_questions = {self.number_of_questions}, range_numbers = {self.range_numbers}")


class NumbersInt(Numbers):
    """
    Quiz with integer numbers
    """
    def __init__(self, name: str = "NumbersInt", number_of_questions: int = None, range_numbers: int = 100):
        super().__init__(name, number_of_questions, range_numbers)

    def get_random_number(self):
        return random.randint(1, self.range_numbers)

    def __repr__(self):
        return (
            f"name = {self.name}, number_of_questions = {self.number_of_questions}, range_numbers = {self.range_numbers}")


class NumbersFloat(Numbers):
    """
    Quiz with float numbers with one decimal number
    """
    def __init__(self, name: str = "NumbersFloat", number_of_questions: int = None, range_numbers: int = 100):
        super().__init__(name, number_of_questions, range_numbers)

    def get_random_number(self):
        return round(random.uniform(1.0, float(self.range_numbers)), 1)

    def __repr__(self):
        return (
            f"name = {self.name}, number_of_questions = {self.number_of_questions}, range_numbers = {self.range_numbers}")


class Letters(Quiz):
    def __init__(self, name: str = "Letters", number_of_questions: int = None):
        super().__init__(name, number_of_questions)

    def get_failures(self, file_path: str):
        try:
            df = pd.read_csv("answered_letters.csv", sep=";", names=["num", "answer", "item"])
            failures = df.loc[df["answer"] == 0]
            return failures["item"].to_list()

        except FileNotFoundError:
            print(f"{file_path} not found!")

    def get_random_letter(self):
        return random.choice(string.ascii_uppercase)

    def __repr__(self):
        return (
            f"name = {self.name}, number_of_questions = {self.number_of_questions}")






























class Quiz2:
    @staticmethod
    def remove_file(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def set_counter(file_path: str):
        with open(file_path, "r") as file:
            lines = file.readlines()
            return len(lines)

    @staticmethod
    def set_correct_answer(file_path: str, i: str):
        with open(file_path, "a+") as file:
            if not i:
                file.write("1;1;X\n")
            else:
                file.write(f"{int(i) + 1};1;X\n")

    @staticmethod
    def set_fail_answer(file_path: str, i: str, answer: str):
        with open(file_path, "a+") as file:
            if not i:
                file.write(f"1;0;{answer}\n")
            else:
                file.write(f"{int(i) + 1};0;{answer}\n")

    @staticmethod
    def failures(file_path: str):
        df = pd.read_csv(file_path, sep=";", names=["num", "answer", "items"], encoding="windows-1250")
        return df["items"].to_list()

    @staticmethod
    def set_temp(file_path: str, key: str, answer: str):
        with open(file_path, "a+", encoding="utf-8") as file:
            file.write(f"{key};{answer}\n")
            file.close()

    @staticmethod
    def read_temp_file(filename: str) -> list:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.readlines()
            data = [i.strip("\n") for i in data]
            data = [i.split(";") for i in data]
            if len(data) < 2:
                return data[-1]
            else:
                return data[-2]

    @staticmethod
    def set_selected_question_set(filename: str, question_set: str):
        with open(filename, "w") as file:
            file.write(question_set)

    @staticmethod
    def get_selected_question_set(filename: str):
        with open(filename, "r") as file:
            data = file.read()
            return data

    @staticmethod
    def get_questions_dict(name: str) -> dict:
        general_questions = {
            "kočka": "Jaké zvíře říká 'mňau'? Nápověda: Je to domácí mazlíček.",
            "slunce": "Co svítí na obloze a dělá den světlým? Nápověda: Je to hvězda.",
            "jabloň": "Jaký strom dává chutné plody? Nápověda: Dáváme je do koláče.",
            "zvíře": "Jaké je obecné slovo pro živé bytosti? Nápověda: Existuje mnoho druhů.",
            "moře": "Jak se jmenuje velká vodní plocha? Nápověda: Může být slané.",
            "hora": "Jak se nazývá vysoká země, pokrytá sněhem? Nápověda: Lidé tam lyžují.",
            "dřevo": "Jaký materiál pochází ze stromů a používá se na nábytek? Nápověda: Je to přírodní materiál.",
            "motýl": "Jaké zvíře se mění z housenky? Nápověda: Může mít krásná křídla.",
            "panda": "Jaké zvíře je černobílé a jí bambus? Nápověda: Žije v Číně.",
            "rybník": "Jak se jmenuje malá vodní plocha, kde žijí ryby? Nápověda: Můžete poblíž vidět lekníny.",
            "slon": "Jaké zvíře má dlouhý chobot? Nápověda: Je to největší suchozemské zvíře.",
            "delfín": "Jaké zvíře žije v moři a skáče nad vodou? Nápověda: Je to inteligentní savec.",
            "hlemýžď": "Jaké zvíře má ulitu na zádech? Nápověda: Je to měkkýš.",
            "pavouk": "Jaké zvíře má osm nohou a pavučiny? Nápověda: Není to hmyz.",
            "fialka": "Jaká květina má modré nebo fialové květy? Nápověda: Je to oblíbená zahradní rostlina.",
            "kaktus": "Jaká rostlina může přežít dlouho bez vody? Nápověda: Má trny.",
            "včela": "Jaké hmyzo opyluje květiny a dává med? Nápověda: Může bodnout.",
            "blesk": "Co se děje na obloze během bouřky, když vidíme záblesky? Nápověda: Může být slyšet hrom.",
            "země": "Jak se jmenuje planeta, na které žijeme? Nápověda: Je modrá a má vodu.",
            "jezero": "Jak se jmenuje velká vodní plocha, kde se lidé mohou koupat? Nápověda: Není to moře.",
            "paprika": "Jaká zelenina je červená, zelená nebo žlutá? Nápověda: Je křupavá.",
            "kůň": "Jaké zvíře je rychlé a často se jezdí? Nápověda: Je to domácí zvíře.",
            "kov": "Jaký materiál je těžký a lesklý? Nápověda: Může být železný nebo měděný.",
            "oheň": "Co dělá teplo a světlo? Nápověda: Může být nebezpečný.",
            "hlava": "Kde máme oči, uši a nos? Nápověda: Je to část těla, kterou používáme k vidění.",
            "strom": "Jaká rostlina má kmen a listy? Nápověda: Může poskytovat stín.",
            "květina": "Jaká rostlina má krásné barevné květy? Nápověda: Můžeme ji darovat.",
            "klokan": "Jaké zvíře skáče a nosí mládě v kapse? Nápověda: Je to australské zvíře.",
            "žirafa": "Jaké zvíře má dlouhý krk a žije na savaně? Nápověda: Jí listy ze stromů.",
            "medvěd": "Jaké zvíře je velké a žije v lesích? Nápověda: Může být hnědý nebo černý.",
            "sníh": "Co padá z nebe v zimě? Nápověda: Můžeme ho koulet do koulí.",
            "bouřka": "Jaký je přírodní jev, kdy slyšíme hrom a vidíme blesk? Nápověda: Může pršet.",
            "zahrada": "Jaké místo máme kolem domu, kde pěstujeme rostliny? Nápověda: Může tam být trávník.",
            "voda": "Jaká tekutina je nezbytná pro život? Nápověda: Můžeme ji pít.",
            "léto": "Jaké roční období je teplé a slunečné? Nápověda: Následuje jaro.",
            "podzim": "Jaké roční období, kdy listy mění barvu? Nápověda: Je to mezi létem a zimou.",
            "hnízdo": "Kde ptáci staví místa pro mláďata? Nápověda: Může být na větvi stromu.",
            "zeměkoule": "Jak se nazývá model naší planety? Nápověda: Můžeme na ní vidět oceány.",
            "měsíc": "Jaký je objekt, který svítí na noční obloze? Nápověda: Můžeme ho vidět v noci.",
            "pohádka": "Jaký příběh je plný fantazie? Nápověda: Děti si je rády poslouchají.",
            "mrak": "Co pluje na obloze a vypadá jako vata? Nápověda: Může pršet.",
            "hvězda": "Co vidíme na noční obloze? Nápověda: Může svítit.",
            "krokodýl": "Jaký plaz žije v řekách a močálech? Nápověda: Je to predátor.",
            "kachna": "Jaké zvíře je vodní pták? Nápověda: Je to často vidět na řece.",
            "krab": "Jaké zvíře má tvrdou skořápku? Nápověda: Má klepeta.",
            "veverka": "Jaké zvíře skáče po stromech? Nápověda: Má huňatý ocas.",
            "lev": "Jaké zvíře je král zvířat? Nápověda: Žije v savaně.",
            "sova": "Jaký pták je známý svým houkáním? Nápověda: Může vidět ve tmě.",
            "rostlina": "Jaký typ organismu žije dva roky? Nápověda: Je to mezi jednoletými a trvalkami.",
            "jelen": "Jaké zvíře má parohy a žije v lese? Nápověda: Je to býložravec.",
            "stín": "Co se tvoří, když je něco mezi námi a světlem? Nápověda: Můžeme je vidět na zemi.",
            "bublina": "Co dělá mýdlo nebo sycené nápoje? Nápověda: Jsou kulaté a lesklé.",
            "mazlíček": "Jak se nazývá malý domácí zvíře? Nápověda: Může to být pes nebo kočka.",
            "pravítko": "Jak se nazývá nástroj na měření? Nápověda: Používá se v matematice.",
            "plyšák": "Jaké hračky jsou měkké a útulné? Nápověda: Děti je rády objímají.",
            "klíč": "Co používáme k odemykání? Nápověda: Mělo by to být kovové.",
            "vlak": "Jaký dopravní prostředek jezdí po kolejích? Nápověda: Může mít mnoho vagónů.",
            "loď": "Jaká vozidla plují po vodě? Nápověda: Můžeme je vidět na řece."
        }
        capital_cities_europe = {"Tirana": "Jaké je hlavní město Albánie? Nápověda: Město začíná písmeny Ti.",
                                 "Andorra la Vella": "Jaké je hlavní město Andorry? Nápověda: Město začíná písmeny An.",
                                 "Jerevan": "Jaké je hlavní město Arménie? Nápověda: Město začíná písmeny Je.",
                                 "Baku": "Jaké je hlavní město Ázerbájdžánu? Nápověda: Město začíná písmeny Ba.",
                                 "Brusel": "Jaké je hlavní město Belgie? Nápověda: Město začíná písmeny Br.",
                                 "Minsk": "Jaké je hlavní město Běloruska? Nápověda: Město začíná písmeny Mi.",
                                 "Sarajevo": "Jaké je hlavní město Bosny a Hercegoviny? Nápověda: Město začíná písmeny Sa.",
                                 "Sofie": "Jaké je hlavní město Bulharska? Nápověda: Město začíná písmeny So.",
                                 "Podgorica": "Jaké je hlavní město Černé Hory? Nápověda: Město začíná písmeny Po.",
                                 "Praha": "Jaké je hlavní město České republiky? Nápověda: Město začíná písmeny Pr.",
                                 "Kodaň": "Jaké je hlavní město Dánska? Nápověda: Město začíná písmeny Ko.",
                                 "Tallinn": "Jaké je hlavní město Estonska? Nápověda: Město začíná písmeny Ta.",
                                 "Helsinky": "Jaké je hlavní město Finska? Nápověda: Město začíná písmeny He.",
                                 "Paříž": "Jaké je hlavní město Francie? Nápověda: Město začíná písmeny Pá.",
                                 "Tbilisi": "Jaké je hlavní město Gruzie? Nápověda: Město začíná písmeny Tb.",
                                 "Amsterodam": "Jaké je hlavní město Holandska? Nápověda: Město začíná písmeny Am.",
                                 "Záhřeb": "Jaké je hlavní město Chorvatska? Nápověda: Město začíná písmeny Zá.",
                                 "Dublin": "Jaké je hlavní město Irska? Nápověda: Město začíná písmeny Du.",
                                 "Reykjavík": "Jaké je hlavní město Islandu? Nápověda: Město začíná písmeny Re.",
                                 "Řím": "Jaké je hlavní město Itálie? Nápověda: Město začíná písmeny Ří.",
                                 "Nur-Sultan": "Jaké je hlavní město Kazachstánu? Nápověda: Město začíná písmeny Nu.",
                                 "Nikósie": "Jaké je hlavní město Kypru? Nápověda: Město začíná písmeny Ni.",
                                 "Kyjev": "Jaké je hlavní město Ukrajiny? Nápověda: Město začíná písmeny Ky.",
                                 "Vilnius": "Jaké je hlavní město Litvy? Nápověda: Město začíná písmeny Vi.",
                                 "Lucemburk": "Jaké je hlavní město Lucemburska? Nápověda: Město začíná písmeny Lu.",
                                 "Budapešť": "Jaké je hlavní město Maďarska? Nápověda: Město začíná písmeny Bu.",
                                 "Valletta": "Jaké je hlavní město Malty? Nápověda: Město začíná písmeny Va.",
                                 "Skopje": "Jaké je hlavní město Severní Makedonie? Nápověda: Město začíná písmeny Sk.",
                                 "Kišinjov": "Jaké je hlavní město Moldavska? Nápověda: Město začíná písmeny Ki.",
                                 "Monako": "Jaké je hlavní město Monaka? Nápověda: Město začíná písmeny Mo.",
                                 "Berlín": "Jaké je hlavní město Německa? Nápověda: Město začíná písmeny Be.",
                                 "Oslo": "Jaké je hlavní město Norska? Nápověda: Město začíná písmeny Os.",
                                 "Varšava": "Jaké je hlavní město Polska? Nápověda: Město začíná písmeny Va.",
                                 "Londýn": "Jaké je hlavní město Spojeného království? Nápověda: Město začíná písmeny Lo.",
                                 "Madrid": "Jaké je hlavní město Španělska? Nápověda: Město začíná písmeny Ma.",
                                 "Bern": "Jaké je hlavní město Švýcarska? Nápověda: Město začíná písmeny Be.",
                                 "Stockholm": "Jaké je hlavní město Švédska? Nápověda: Město začíná písmeny St.",
                                 "Atény": "Jaké je hlavní město Řecka? Nápověda: Město začíná písmeny At.",
                                 "Moskva": "Jaké je hlavní město Ruska? Nápověda: Město začíná písmeny Mo.",
                                 "Vatikán": "Jaké je hlavní město Vatikánu? Nápověda: Město začíná písmeny Va.",
                                 "Bělehrad": "Jaké je hlavní město Srbska? Nápověda: Město začíná písmeny Bě.",
                                 }

        if name == "capital_cities_europe":
            return capital_cities_europe
        elif name == "general_questions":
            return general_questions
