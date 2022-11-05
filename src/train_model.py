import numpy as np
import pandas as pd
from sklearn import naive_bayes
from sklearn import datasets
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import _pickle as cPickle
from sklearn import preprocessing


class DataLoader:
    def __init__(self):  # array: data - time - features - has crimed - type_data
        osm_data = pd.read_csv("data/osm/osm_data_cell.csv")
        columns_to_drop = osm_data.sum(axis=0) > 
        columns_to_drop[:2] = True
        print(osm_data.loc[:, -columns_to_drop])

        osm_data = osm_data.loc[:, columns_to_drop]
        uk_data = pd.read_csv("data/uk_police_data/uk_police_data_cell.csv")
        uk_police_data = pd.get_dummies(uk_data)
        uk_police_data["crime_case"] = uk_police_data.iloc[:, 2:].sum(axis=1)
        uk_police_data_sum = uk_police_data.loc[:, ["cell_id", "crime_case"]]
        data_out = pd.merge(osm_data, uk_police_data_sum, on="cell_id", how="outer")
        self.datasource = data_out.fillna(0)

        x = self.datasource.values  # returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        self.datasource = pd.DataFrame(x_scaled)
        self.datasource.to_csv("data.csv")

        self.datasource["is_train"] = (
            np.random.uniform(0, 1, len(self.datasource)) <= 0.75
        )
        self.y_name = np.array(["crime_case"])

    def load_data(self):
        train = self.datasource[self.datasource["is_train"] == True]
        test = self.datasource[self.datasource["is_train"] == False]
        return (
            train[train.columns[2:-1]],
            train[train.columns[-1]],
            test[test.columns[2:-1]],
            test[test.columns[-1]],
        )


def main():
    X_train, y_train, X_test, y_test = DataLoader().load_data()
    # 1
    model_BernoulliNB = naive_bayes.BernoulliNB()
    model_BernoulliNB.fit(X_train, y_train)
    predicted_y = model_BernoulliNB.predict(X_test)

    print(metrics.classification_report(y_test, predicted_y))

    # with open("./model/model_BernoulliNB.pkl", "wb") as fid:
    #     cPickle.dump(model_BernoulliNB, fid)


if __name__ == "__main__":
    main()

"""

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

"""
