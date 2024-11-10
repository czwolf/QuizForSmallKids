# import string
# import random
#
# letter = random.choice(string.ascii_uppercase)
#
# print(letter)

import pandas as pd
df = pd.read_csv("numbers.csv", sep=";", names=["num", "answer", "item"])
# df.fillna("A")
# df["answer"] = df["answer"].astype(int)
# df["item"] = df["item"].astype(str)
num_of_questions = len(df)
answer_correct = df["answer"].sum()
answer_failed = num_of_questions - answer_correct
percentage_correct = (answer_correct / num_of_questions) * 100
percentage_failed = (answer_failed / num_of_questions) * 100

print(df)
print(answer_correct)
