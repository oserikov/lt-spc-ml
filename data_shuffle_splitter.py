import csv
import warnings

from tools.utils import train_test_val_split

warnings.filterwarnings("ignore", category=FutureWarning)


def split_original_csv_to_train_test_val_csv(original_data_filename, original_data_csv_headless=False,
                                             train_data_filename="train.csv", test_data_filename="test.csv", val_data_filename="val.csv",
                                             train_part_in_percents=0.66, val_part_of_test_part_in_percents=0.66):
    def ids_loader(filename, headless=False):
        ids_loaded = []
        with open(filename, 'r', encoding="utf-8") as data_csv_file:
            ids_containing_file_reader = csv.reader(data_csv_file, quoting=csv.QUOTE_NONNUMERIC)
            if not headless:
                next(ids_containing_file_reader, None)
            for id_containing_row in ids_containing_file_reader:
                ids_loaded.append(int(id_containing_row[0]))
        return ids_loaded

    ids = list(set(ids_loader(original_data_filename, headless=original_data_csv_headless)))

    train_ids, test_ids, val_ids = train_test_val_split(ids,
                                                        train_part_in_percents=train_part_in_percents,
                                                        val_part_of_test_part_in_percents=val_part_of_test_part_in_percents)
    train_ids = set(train_ids)
    test_ids = set(test_ids)
    val_ids = set(val_ids)

    with open(original_data_filename, 'r', encoding="utf-8") as original_data_csv_file, \
            open(train_data_filename, 'w', encoding="utf-8") as train_data_csv_file, \
            open(test_data_filename, 'w', encoding="utf-8") as test_data_csv_file, \
            open(val_data_filename, 'w', encoding="utf-8") as val_data_csv_file:

        original_data_reader = csv.reader(original_data_csv_file, quoting=csv.QUOTE_NONNUMERIC)
        if not original_data_csv_headless:
            next(original_data_reader, None)

        train_data_writer = csv.writer(train_data_csv_file, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n")
        test_data_writer = csv.writer(test_data_csv_file, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n")
        val_data_writer = csv.writer(val_data_csv_file, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n")

        writer = None
        for row in original_data_reader:
            if int(row[0]) in train_ids:
                writer = train_data_writer
            elif int(row[0]) in test_ids:
                writer = test_data_writer
            elif int(row[0]) in val_ids:
                writer = val_data_writer
            writer.writerow(row)
