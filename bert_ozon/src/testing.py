from src.dataset import tokenizer
import torch


def predict_similarity(sentence_pair, model):
    test_input = tokenizer(sentence_pair, padding='max_length', max_length=128, truncation=True, return_tensors="pt")
    test_input['input_ids'] = test_input['input_ids']
    test_input['attention_mask'] = test_input['attention_mask']
    del test_input['token_type_ids']
    output = model(test_input)
    sim = torch.nn.functional.cosine_similarity(output[0], output[1], dim=0).item()
    return sim
