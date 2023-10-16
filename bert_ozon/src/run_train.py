from datasets import load_dataset
from src.dataset import STSBDataset
from model import BertForSTS
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
import torch
from torch.utils.data import DataLoader
import time
import pandas as pd

from dataset_.create_dataset import STSBDataset
from testing import predict_similarity
from sklearn.model_selection import train_test_split
from src.train import train

path_info_with_sim = "/bert_ozon/data/csv_with_similarity_score/info_with_sim.csv"


if __name__ == '__main__':

    # if torch.cuda.is_available():
    #     device = torch.device("cuda")
    # else:
    #     device = torch.device("cpu")
    device = torch.device("cpu")

    df = pd.read_csv(path_info_with_sim, delimiter=',', index_col=False)
    train_ds, test_ds = train_test_split(df, test_size=0.2, random_state=0)
    train_ds = STSBDataset(train_ds)
    test_ds = STSBDataset(test_ds)

    model = BertForSTS()

    batch_size = 8

    train_dataloader = DataLoader(
        train_ds,
        num_workers=4,
        batch_size=batch_size,
        shuffle=True
    )

    validation_dataloader = DataLoader(
        test_ds,
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
    model, training_stats = train(model=model,
                                  device=device,
                                  optimizer=optimizer,
                                  scheduler=scheduler,
                                  train_dataloader=train_dataloader,
                                  validation_dataloader=validation_dataloader,
                                  epochs=epochs)


