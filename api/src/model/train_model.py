import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class DataFormat:
    def __init__(self, data_source):  # array: data - time - features - has crimed - type_data
        self.datasource = data_source

    def load_data(self, type_data):
        return []


input_ = torch.randn(100, 48, 10)  # 100 input data - in 48 hours (can fix depend on time) - 10 features
target_ = torch.randint(0, 2, (100,))  # binary output


class LSTMClassification(nn.Module):

    def __init__(self, input_dim, hidden_dim, target_size):
        super(LSTMClassification, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, target_size)

    def forward(self, input_):
        lstm_out, (h, c) = self.lstm(input_)
        logits = self.fc(lstm_out[-1])
        scores = F.sigmoid(logits)
        return scores


class TrainModel:
    def __init__(self):
        self.model = LSTMClassification(input_.shape[2],
                                        hidden_dim=6,
                                        target_size=1)
        self.epochs = 10
        data = DataFormat("")
        self.train_loader = data.load_data(type_data="train")
        self.test_loader = data.load_data(type_data="test")

    def train(self):
        loss_function = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.1)

        history = {
            'loss': []
        }
        for epoch in range(self.epochs):
            losses = []
            for i, data in enumerate(self.train_loader, 0):
                inputs, labels = data
                self.zero_grad()
                tag_scores = self.model(inputs)
                labels = labels.unsqueeze(1)
                loss = loss_function(tag_scores, labels)
                loss.backward()
                optimizer.step()
                losses.append(float(loss))
            avg_loss = np.mean(losses)
            history['loss'].append(avg_loss)
            print("Epoch {} / {}: Loss = {:.3f}".format(epoch + 1, self.epochs, avg_loss))
        return history

    def test(self):
        predicts, labels = [], []
        for i, data in enumerate(self.test_loader, 0):
            inputs, labels = data
            predicts += self.model(inputs)
            labels += labels.unsqueeze(1)
        accuracy = np.sum(predicts == labels) / len(self.test_loader)
        print(accuracy)


def main():
    pass


if __name__ == "__main__":
    main()
