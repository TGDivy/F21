import numpy as np
import pandas as pd
from sklearn import naive_bayes
from sklearn import datasets
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import _pickle as cPickle

class DataLoader:
    def __init__(self, data_source):  # array: data - time - features - has crimed - type_data
        self.datasource = pd.read_csv(data_source)
        self.datasource['is_train'] = np.random.uniform(0, 1, len(self.datasource)) <= 0.75
        print(self.datasource)
        self.y_name = np.array(['hotspot'])

    def load_data(self):
        train = self.datasource[self.datasource['is_train']==True]
        test = self.datasource[self.datasource['is_train']==False]
        print(train[train.columns[1:8]],  train[train.columns[0]], test[test.columns[1:8]],  test[test.columns[0]])
        return train[train.columns[1:8]],  train[train.columns[0]], test[test.columns[1:8]],  test[test.columns[0]]


# class LSTMClassification(nn.Module):
#
#     def __init__(self, input_dim, hidden_dim, target_size):
#         super(LSTMClassification, self).__init__()
#         self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
#         self.fc = nn.Linear(hidden_dim, target_size)
#
#     def forward(self, input_):
#         lstm_out, (h, c) = self.lstm(input_)
#         logits = self.fc(lstm_out[-1])
#         scores = F.sigmoid(logits)
#         return scores

# class TrainModel:
#     def __init__(self):
#         self.model = LSTMClassification(input_.shape[2],
#                                         hidden_dim=6,
#                                         target_size=1)
#         self.epochs = 10
#         data = DataFormat("")
#         self.train_loader = data.load_data(type_data="train")
#         self.test_loader = data.load_data(type_data="test")
#
#     def train(self):
#         loss_function = nn.BCEWithLogitsLoss()
#         optimizer = torch.optim.SGD(self.model.parameters(), lr=0.1)
#
#         history = {
#             'loss': []
#         }
#         for epoch in range(self.epochs):
#             losses = []
#             for i, data in enumerate(self.train_loader, 0):
#                 inputs, labels = data
#                 self.zero_grad()
#                 tag_scores = self.model(inputs)
#                 labels = labels.unsqueeze(1)
#                 loss = loss_function(tag_scores, labels)
#                 loss.backward()
#                 optimizer.step()
#                 losses.append(float(loss))
#             avg_loss = np.mean(losses)
#             history['loss'].append(avg_loss)
#             print("Epoch {} / {}: Loss = {:.3f}".format(epoch + 1, self.epochs, avg_loss))
#         return history
#
#     def test(self):
#         predicts, labels = [], []
#         for i, data in enumerate(self.test_loader, 0):
#             inputs, labels = data
#             predicts += self.model(inputs)
#             labels += labels.unsqueeze(1)
#         accuracy = np.sum(predicts == labels) / len(self.test_loader)
#         print(accuracy)


def main():
    X_train, y_train, X_test, y_test = DataLoader("../data/sampletrain.csv").load_data()
    # 1
    model_BernoulliNB = naive_bayes.BernoulliNB()
    model_BernoulliNB.fit(X_train, y_train)
    predicted_y = model_BernoulliNB.predict(X_test)
    print(metrics.classification_report(y_test, predicted_y))
    with open('./model/model_BernoulliNB.pkl', 'wb') as fid:
        cPickle.dump(model_BernoulliNB, fid)
    # 2
    model_MultinomialNB = naive_bayes.MultinomialNB()
    model_MultinomialNB.fit(X_train, y_train)
    predicted_y_MultinomialNB = model_MultinomialNB.predict(X_test)
    print(metrics.classification_report(y_test, predicted_y_MultinomialNB))
    with open('./model/model_MultinomialNB.pkl', 'wb') as fid:
        cPickle.dump(model_MultinomialNB, fid)

    # load model:
    # with open('my_dumped_classifier.pkl', 'rb') as fid:
    #     gnb_loaded = cPickle.load(fid)


if __name__ == "__main__":
    main()
