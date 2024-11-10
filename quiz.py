import pandas as pd
import os

class Quiz:

    @staticmethod
    def remove_file(file_name: str):
        if os.path.exists(file_name):
            os.remove(file_name)

    @staticmethod
    def set_counter(file_name: str):
        with open(file_name, "r") as file:
            lines = file.readlines()
            return len(lines)

    @staticmethod
    def set_correct_answer(file_name: str, i: str):
        with open(file_name, "a+") as file:
            if not i:
                file.write("1;1;X\n")
            else:
                file.write(f"{int(i) + 1};1;X\n")

    @staticmethod
    def set_fail_answer(file_name: str, i: str, answer: str):
        with open(file_name, "a+") as file:
            if not i:
                file.write(f"1;0;{answer}\n")
            else:
                file.write(f"{int(i) + 1};0;{answer}\n")

    @staticmethod
    def failures(file_name: str):
        df = pd.read_csv(file_name, sep=";", names=["num", "answer", "items"], encoding="windows-1250")
        return df["items"].to_list()
