import pandas as pd
import random
from src.model import BertForSTS
from src.testing import predict_similarity
from pathlib import Path
root_dir = Path(__file__).parent.parent.parent.resolve()  # directory of source root

path_info_clean = "bert_ozon/data/csv/info_clean.csv"
path_info_with_sim = "bert_ozon/data/csv_with_similarity_score/info_with_sim.csv"
path_info_with_sim_neg = "bert_ozon/data/csv_with_similarity_score/info_with_sim_neg.csv"


def add_sim_score():
    df = pd.read_csv(path_info_clean, delimiter=',', index_col=False)

    df["ИндексПохожести"] = [1] * len(df)
    df.to_csv(path_info_with_sim, encoding='utf-8', index=False)


def add_neg_class():
    df = pd.read_csv(path_info_with_sim, delimiter=',', index_col=False)
    df_neg = pd.DataFrame()

    model = BertForSTS()

    category_list = []
    description_list = []
    sim_score_list = []

    # df1 = df["Категория"][:100]
    length = len(df)
    print(length)
    for i, sentence1 in enumerate(df["Категория"]):
        print(i)
        rand_list = random.sample(range(0, length), 7)

        sentences2_list = [df["Категория"][i] for i in rand_list]
        score = []
        for sentence2 in sentences2_list:
            sentence_pair = [sentence1, sentence2]
            sim = predict_similarity(sentence_pair, model)
            score.append(sim)

        min_val = min(score)
        min_idx = score.index(min_val)

        categ = sentences2_list[min_idx]  # выбрали наиболее непохожую категорию
        category_list.append(categ)
        description_list.append(df["НазваниеОписание"][i])
        sim_score_list.append(0)

    df_neg["НазваниеОписание"] = description_list
    df_neg["Категория"] = category_list
    df_neg["ИндексПохожести"] = sim_score_list

    df_final = pd.concat([df, df_neg], axis=0)
    df_final = df_final.sample(frac=1)
    df_final.to_csv(path_info_with_sim_neg, encoding='utf-8', index=False)


if __name__ == '__main__':
    # add_sim_score()
    # test()
    add_neg_class()
