from transformers import BertTokenizer
import torch
from torch.utils.data import DataLoader


tokenizer = BertTokenizer.from_pretrained('cointegrated/rubert-tiny')


class STSBDataset(torch.utils.data.Dataset):

    def __init__(self, dataset):
        # Normalize the similarity scores in the dataset
        self.similarity_scores = [float(i) for i in dataset["ИндексПохожести"]]
        self.first_sentences = [i for i in dataset["НазваниеОписание"]]
        self.second_sentences = [i for i in dataset["Категория"]]
        self.concatenated_sentences = [[str(x), str(y)] for x, y in zip(self.first_sentences, self.second_sentences)]

    def __len__(self):
        return len(self.concatenated_sentences)

    def get_batch_labels(self, idx):
        return torch.tensor(self.similarity_scores[idx])

    def get_batch_texts(self, idx):
        return tokenizer(self.concatenated_sentences[idx], padding='max_length', max_length=128, truncation=True, return_tensors="pt")

    def __getitem__(self, idx):
        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)
        return batch_texts, batch_y


def collate_fn(texts):
    input_ids = texts['input_ids']
    attention_masks = texts['attention_mask']
    features = [{'input_ids': input_id, 'attention_mask': attention_mask}
                for input_id, attention_mask in zip(input_ids, attention_masks)]
    return features