from datasets import load_dataset
from src.dataset import STSBDataset
from model import BertForSTS
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
import torch
from torch.utils.data import DataLoader
import time

from testing import predict_similarity

if __name__ == '__main__':

    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    dataset = load_dataset("stsb_multi_mt", "en")
    print(dataset['train'])

    # print(train_ds.first_sentences[0])
    # print(train_ds.second_sentences[0])
    # print(train_ds.concatenated_sentences[0])
    # print(dataset['train']['sentence1'][0])

    # batch_texts, batch_y = train_ds[0]
    # print(batch_texts, batch_y)

    model = BertForSTS()

    train_ds = STSBDataset(dataset['train'])
    sentence_pair = train_ds.concatenated_sentences[50]
    # sentence_pair = ["", ""]
    sim = predict_similarity(sentence_pair, model)
    # print(sim)

    # Create dataloader
    train_ds = STSBDataset(dataset['train'])
    val_ds = STSBDataset(dataset['dev'])

    batch_size = 8

    train_dataloader = DataLoader(
        train_ds,
        num_workers=4,
        batch_size=batch_size,
        shuffle=True
    )

    validation_dataloader = DataLoader(
        val_ds,
        num_workers=4,
        batch_size=batch_size
    )

    # Chose optimizer
    optimizer = AdamW(model.parameters(),
                      lr=1e-6)

    # Create scheduler
    epochs = 10
    # Total number of training steps is [number of batches] x [number of epochs].
    total_steps = len(train_dataloader) * epochs
    scheduler = get_linear_schedule_with_warmup(optimizer,
                                                num_warmup_steps=0,
                                                num_training_steps=total_steps)

    # Train model
    # model, training_stats = train(model=model,
    #                               device=device,
    #                               optimizer=optimizer,
    #                               scheduler=scheduler,
    #                               train_dataloader=train_dataloader,
    #                               validation_dataloader=validation_dataloader,
    #                               epochs=epochs)


    # sentence_pair = ["haberdashery jewelry bags backpacks suitcases unisex backpack",
    #                  "unisex backpack sports backpack sports unisex sports backpack classic plain backpack in discreet colors will become an indispensable companion for active youth who appreciate"]
    # sim = predict_similarity(sentence_pair, model)
    # print(sim)
    #
    # sentence_pair = ["haberdashery jewelry bags backpacks suitcases suitcase for children",
    #                  "unisex backpack sports backpack sports unisex sports backpack classic plain backpack in discreet colors will become an indispensable companion for active youth who appreciate"]
    # sim = predict_similarity(sentence_pair, model)
    # print(sim)
    #
    # sentence_pair = ["haberdashery jewelry bags backpacks suitcases medical bag",
    #                  "unisex backpack sports backpack sports unisex sports backpack classic plain backpack in discreet colors will become an indispensable companion for active youth who appreciate"]
    # sim = predict_similarity(sentence_pair, model)
    # print(sim)