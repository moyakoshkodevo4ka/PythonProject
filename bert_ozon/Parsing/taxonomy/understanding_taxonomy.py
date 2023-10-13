import json


def create_categories3_list():
    path = "/home/mikhail/Projects/bert_ozon/Parsing/collecting_data/taxonomy/ozon_taxonomy_api.json"
    with open(path, 'r') as fp:
        data = json.load(fp)

    categories3_info_list = []

    categories1 = data['result']

    for category1 in categories1:
        level1_title = category1['title']
        categories2 = category1['children']

        for category2 in categories2:
            level2_title = category2['title']
            categories3 = category2['children']

            for category3 in categories3:
                level3_title = category3['title']
                categories3_info_list.append(level3_title)

        categories3_info_list.append('\n')

    path = "/home/mikhail/Projects/bert_ozon/Parsing/collecting_data/taxonomy/categories3_list.txt"
    with open(path, 'w') as f:
        for item in categories3_info_list:
            # fp.write(item + '\n')
            f.writelines("%s\n" % item)


def create_full_categories_list():
    path = "/home/mikhail/Projects/bert_ozon/Parsing/collecting_data/taxonomy/ozon_taxonomy_api.json"
    with open(path, 'r') as fp:
        data = json.load(fp)

    categories3_info_list = []

    categories1 = data['result']

    for category1 in categories1:
        level1_title = category1['title']
        categories2 = category1['children']

        for category2 in categories2:
            level2_title = category2['title']
            categories3 = category2['children']

            for category3 in categories3:
                level3_title = category3['title']
                categories3_info_list.append(level1_title + '/' + level2_title + '/' + level3_title)

        # categories3_info_list.append('\n')

    path = "/home/mikhail/Projects/bert_ozon/Parsing/collecting_data/taxonomy/full_categories.txt"
    with open(path, 'w') as f:
        for item in categories3_info_list:
            # fp.write(item + '\n')
            f.writelines("%s\n" % item)


if __name__ == '__main__':
    # создаем txt файл с категориями 3-го уровня
    # create_categories3_list()

    create_full_categories_list()
