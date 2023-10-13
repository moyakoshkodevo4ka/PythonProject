"""
создает csv обработанных и необработанных категорий

def parse_categories(self):
    df1 = pd.DataFrame()
    ne_obrab = []
    obrab = []
    fp = open("/bert_ozon/Parsing/collecting_data/taxonomy/full_categories.txt", 'r')
    i = 0
    for line in fp:
        print(i)
        i += 1
        ne_obrab.append([line[:-1]])

        info = {"description": [line[:-1]]}
        df = pd.DataFrame(info)
        data = df["description"].apply(self.lemmatize)
        word_list = data[0]

        product_info = ' '.join(word_list)

        obrab.append(product_info)

    df1["Категории"] = ne_obrab
    df1["ОбработанныеКатегории"] = obrab

    df1.to_csv("/bert_ozon/src/TESTING/categories.csv", encoding='utf-8', index=False)
"""