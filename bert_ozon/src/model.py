import torch
from sentence_transformers import SentenceTransformer, models

'cointegrated/rubert-tiny'
'bert-base-uncased'
class BertForSTS(torch.nn.Module):

    def __init__(self):
        super(BertForSTS, self).__init__()
        self.bert = models.Transformer('bert-base-uncased', max_seq_length=128)
        self.pooling_layer = models.Pooling(self.bert.get_word_embedding_dimension())
        self.sts_bert = SentenceTransformer(modules=[self.bert, self.pooling_layer])

    def forward(self, input_data):
        """
        :param input_data: dict('input_ids': tensor([2, 128]), 'attention_mask': tensor([2, 128]))
        :return: tensor ([2, 768])
        """
        output = self.sts_bert(input_data)['sentence_embedding']
        return output
