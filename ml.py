import csv
import numpy as np
import xgboost as xgb

from tools.utils import read_csv


# noinspection PyPep8Naming
def load_data(filename, left_bound=0):
    X = []
    y = []
    for row in read_csv(filename):
        X.append([float(i) for i in row[left_bound:-1]])
        y.append(float(row[-1]))
    X = np.asarray(X)
    y = np.asarray(y)
    return X, y


# noinspection PyPep8Naming
def train_model(train_data_filename, param, num_round, left_bound=0):
    X_train, y_train = load_data(train_data_filename, left_bound=left_bound)
    train_data_matrix = xgb.DMatrix(X_train, label=y_train)
    return xgb.train(param, train_data_matrix, num_round)


# noinspection PyPep8Naming
def predict(data_filename, bst, left_bound=0):
    X_val, _ = load_data(data_filename, left_bound=left_bound)
    val_data_matrix = xgb.DMatrix(X_val)
    return bst.predict(val_data_matrix)


def predict_to_csv(input_filename, model, output_filename, left_bound=0):
    with open(output_filename, 'w', encoding="utf-8") as val_predicted_csv_file:
        public_features_writer = csv.writer(val_predicted_csv_file, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n")
        for row, proba in zip(read_csv(input_filename), predict(input_filename, model, left_bound=left_bound)):
            row.append(proba)
            public_features_writer.writerow(row)


def save_model(model, filename):
    model.save_model(filename)
    # model.dump_model(filename + ".dump.txt")

    with open(filename+".features", 'w') as outfile:
        [outfile.write('{0}\t{1}\tq\n'.format(i, feat)) for i, feat in enumerate(model.feature_names)]


def ml(train_data_filename, val_data_filename, val_predicted_data_filename, output_model_filename, first_column_id=False):
    training_params = {'silent': 0, 'objective': 'binary:logistic', 'n_jobs':-1}
    num_round = 20
    model = train_model(train_data_filename, training_params, num_round, 1 if first_column_id else 0)
    predict_to_csv(val_data_filename, model, val_predicted_data_filename, 1 if first_column_id else 0)
    save_model(model, output_model_filename)


if __name__ == '__main__':
    ml("train.csv", "val.csv", "val_pred.csv", "xgb.model")
