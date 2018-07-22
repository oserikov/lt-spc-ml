import csv

from sklearn.model_selection import train_test_split


def read_csv_dict(filename, fieldnames):
    with open(filename, encoding="utf-8", errors="backslashreplace") as csv_file:
        for row in csv.DictReader(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC):
            yield row


def sub_dict(some_dict, some_keys, default=None):
    return dict([(k, some_dict.get(k, default)) for k in some_keys])


def train_test_val_split(data, train_part_in_percents=0.66, val_part_of_test_part_in_percents=0.66):
    train_data, test_data = train_test_split(data, train_size=train_part_in_percents, shuffle=True)
    test_data, val_data = train_test_split(test_data, test_size=val_part_of_test_part_in_percents, shuffle=False)

    if len(data) != len(train_data) + len(test_data) + len(val_data):
        raise RuntimeError("splitted data summary size is not equal to the original data's size")

    return train_data, test_data, val_data


def read_csv(filename):
    with open(filename, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            yield row


