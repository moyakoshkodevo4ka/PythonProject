import torch
from src.dataset import collate_fn
from src.criterion import CosineSimilarityLoss
from tqdm import tqdm
import random


def train(model, device, optimizer, scheduler, train_dataloader, validation_dataloader, epochs=10):
    seed_val = 42

    criterion = CosineSimilarityLoss()
    criterion = criterion.to(device)

    random.seed(seed_val)
    torch.manual_seed(seed_val)

    training_stats = []

    for epoch in range(0, epochs):

        # Training

        print("")
        print('======== Epoch {:} / {:} ========'.format(epoch + 1, epochs))
        print('Training...')

        total_train_loss = 0

        model.train()

        # For each batch of training data...
        for train_data, train_label in tqdm(train_dataloader):
            train_data['input_ids'] = train_data['input_ids'].to(device)
            train_data['attention_mask'] = train_data['attention_mask'].to(device)

            train_data = collate_fn(train_data)
            model.zero_grad()

            output = [model(feature) for feature in train_data]

            loss = criterion(output, train_label.to(device))
            total_train_loss += loss.item()

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()

        # Calculate the average loss over all the batches.
        avg_train_loss = total_train_loss / len(train_dataloader)

        print("")
        print("  Average training loss: {0:.5f}".format(avg_train_loss))

        #  Validation

        print("")
        print("Running Validation...")

        total_eval_loss = 0

        model.eval()

        # Evaluate data for one epoch
        for val_data, val_label in tqdm(validation_dataloader):
            val_data['input_ids'] = val_data['input_ids'].to(device)
            val_data['attention_mask'] = val_data['attention_mask'].to(device)

            val_data = collate_fn(val_data)

            with torch.no_grad():
                output = [model(feature) for feature in val_data]

            loss = criterion(output, val_label.to(device))
            total_eval_loss += loss.item()

        # Calculate the average loss over all the batches.
        avg_val_loss = total_eval_loss / len(validation_dataloader)

        print("  Validation Loss: {0:.5f}".format(avg_val_loss))

        # Record all statistics from this epoch.
        training_stats.append(
            {
                'epoch': epoch + 1,
                'Training Loss': avg_train_loss,
                'Valid. Loss': avg_val_loss,
            }
        )

    print("")
    print("Training complete!")

    return model, training_stats
