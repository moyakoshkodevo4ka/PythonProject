import csv
import json
import pandas as pd
import re
from pymorphy2 import MorphAnalyzer
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


path_info_csv = "bert_ozon/data/csv/info.csv"
path_info_clean_csv = "bert_ozon/data/csv/info_clean.csv"

path_1_233 = "bert_ozon/data/1-233/1-233.json"
path_236_998 = "bert_ozon/data/236-998/236-998.json"
path_1001_1741 = "bert_ozon/data/1001-1741/1001-1741.json"

paths = [path_1_233, path_236_998, path_1001_1741]

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()


def create_info_csv():
    with open(path_info_csv, mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",",)
        file_writer.writerow(["НазваниеОписание", "Категория"])

        for path in paths:
            fp = open(path, 'r')
            data = json.load(fp)
            keys = list(data.keys())
            for key in keys:
                name_description = data[key]["name"] + " " + data[key]["description"]
                name_description = name_description.replace("\n", " ")

                category = data[key]["categories"][0]["name"] + " "
                category += data[key]["categories"][1]["name"] + " "
                category += data[key]["categories"][2]["name"]
                category = category.replace("\n", " ")

                file_writer.writerow([name_description, category])


def lemmatize(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]

            tokens.append(token)
    if len(tokens) > 2:
        return tokens
    return None


def clear_csv():
    df = pd.read_csv(path_info_csv, delimiter=',', index_col=False)
    df1 = df["НазваниеОписание"]
    data1 = df1.apply(lemmatize)  # пандас из списков

    df2 = df["Категория"]
    data2 = df2.apply(lemmatize)  # пандас из списков

    data1_list = []
    data2_list = []

    length = len(data1)
    for i in range(length):
        row_list = data1.iloc[i]
        message = delete_short_words_and_empty_strings(row_list)
        if message == 'None':
            print('None ', i)
        elif message == 'delete row':
            print('delete row ', i)
            pass
        else:
            row = message
            data1_list.append([row])
            data2_list.append([' '.join(data2.iloc[i])])
    print(data1_list)
    print(data2_list)

    data1_final = pd.DataFrame(data1_list, columns=["НазваниеОписание"])
    data2_final = pd.DataFrame(data2_list, columns=["Категория"])

    data = pd.concat([data1_final, data2_final], join='outer', axis=1)
    data.to_csv(path_info_clean_csv, encoding='utf-8', index=False)
    
    
def delete_short_words_and_empty_strings(row):
    if row is None:
        return 'None'
    if len(row) < 5:  # кол-во слов в описании
        return 'delete row'
    for word in row:
        if len(word) < 3:
            row.remove(word)
    from_list_to_string = ' '.join(row)
    return from_list_to_string


if __name__ == '__main__':
    # create_info_csv()
    clear_csv()



