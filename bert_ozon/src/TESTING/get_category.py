from src.model import BertForSTS
import torch
import nltk
from nltk.corpus import stopwords
import pandas as pd
import re
from pymorphy2 import MorphAnalyzer
from transformers import BertTokenizer
from tqdm import tqdm
# from googletrans import Translator, constants
from translate import Translator


class Predictor:
    def __init__(self, model_weights_path, categories_list_path):
        self.model = BertForSTS()
        # state_dict = torch.load(model_weights_path)
        # self.model.load_state_dict(state_dict=state_dict)

        self.categories_list_path = categories_list_path
        nltk.download('stopwords')
        self.patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
        self.stopwords_ru = stopwords.words("russian")
        self.morph = MorphAnalyzer()
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.categories = self.__parse_categories__

    def get_prediction(self, product: dict, k: int):
        assert product["marketplace"] == 'OZON'
        product_info = self.prepare(product)

        sim_score = []
        for category in tqdm(self.categories[1]):
            sentence_pair = [product_info, category]
            sim = self.predict_similarity(sentence_pair, self.model)
            sim_score.append(sim)
        top_k = [{"category: ": self.categories[0][sim_score.index(x)], "score: ": x} for x in sorted(sim_score)[-k:]]
        return top_k

    def predict_similarity(self, sentence_pair, model):
        test_input = self.tokenizer(sentence_pair, padding='max_length', max_length=128, truncation=True,
                                    return_tensors="pt")
        test_input['input_ids'] = test_input['input_ids']
        test_input['attention_mask'] = test_input['attention_mask']
        del test_input['token_type_ids']
        output = model(test_input)
        sim = torch.nn.functional.cosine_similarity(output[0], output[1], dim=0).item()
        return sim

    def lemmatize(self, doc):
        doc = re.sub(self.patterns, ' ', doc)
        tokens = []
        for token in doc.split():
            if token and token not in self.stopwords_ru:
                token = token.strip()
                token = self.morph.normal_forms(token)[0]

                tokens.append(token)
        if len(tokens) > 2:
            return tokens
        return None

    @property
    def __parse_categories__(self):
        df = pd.read_csv(self.categories_list_path, delimiter=',', index_col=False)
        return [df['Категории'], df['Обработанные категории']]

    def prepare(self, product):
        description = product["name"] + " " + product["description"]
        info = {"description": [description]}
        df = pd.DataFrame(info)
        data = df["description"].apply(self.lemmatize)
        word_list = data[0]
        product_info = ' '.join(word_list)
        return product_info


if __name__ == '__main__':
    dictionary = {"name": "рюкзак женский светлый / рюкзак женский белый / рюкзак женский бежевый / рюкзак женский кожаный / рюкзак женский спортивный / модный женский рюкзак",
                  "description": "Женский рюкзак из премиальной экокожи, мягкий и удобный.<br/><br/>Дизайн рюкзака выделяется из толпы!<br/><br/>Легкий и вместительный, с большим количеством карманов.<br/><br/>Во внутреннем отделении есть дополнительный карман на молнии.&nbsp;<br/><br/>Удобная и практичная сумка рюкзак подходит для повседневного использования.<br/><br/>Загрязнения на рюкзаке легко отмываются мыльной губкой.",
                  "size": None,
                  "marketplace": "OZON"}

    model_weights_path = ''
    categories_list_path = "/home/mikhail/Projects/bert_ozon/src/TESTING/categories.csv"
    predictor = Predictor(model_weights_path=model_weights_path, categories_list_path=categories_list_path)
    top_k = predictor.get_prediction(dictionary, 5)
    print(top_k)

    # translator = Translator(from_lang="Russian", to_lang="English")
    # product_info = translator.translate("продукт питание")
    # print(product_info)

    # from src.testing import predict_similarity
    # model = BertForSTS()
    # sen1 = predictor.prepare(dictionary)
    # print(sen1)
    # sen1 = "backpack women light backpack women white backpack women beige backpack women leather backpack women sports fashionable women backpack women backpack premium eco-leather soft comfortable design backpack stands out in the crowd light roomy more pocket in the internal compartment additional pocket zipper convenient practical bag backpack suitable for everyday use dirt backpack easy to "
    # s = "продукт питание безалкогольный вино шампанский игристый вино креман партнёр"
    # s_en = "haberdashery decoration glasses frame sunglasses male"
    # a = "галантерея украшение сумка рюкзак чемодан рюкзак женский"
    # a_en = "haberdashery decoration bag backpack suitcase backpack women"
    # sim = predict_similarity([sen1, s_en], model)
    # print(sim)
    # sim = predict_similarity([sen1, a_en], model)
    # print(sim)


