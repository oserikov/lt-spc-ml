import csv
import os

# noinspection PyUnresolvedReferences
from tools.csv_fields_names import all_field_names, public_field_names


class FileUtil:

    writers = None
    open_files = None
    all_features_filename = None
    public_features_filename = None
    bad_records_filename = None
    files_names = []

    def __init__(self, all_features_filename, public_features_filename, bad_records_filename):
        self.writers = {}
        self.open_files = []
        self.all_features_filename = all_features_filename
        self.public_features_filename = public_features_filename
        self.bad_records_filename = bad_records_filename
        self.files_names = [self.bad_records_filename, self.public_features_filename, self.all_features_filename]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for file in self.open_files:
            file.close()

    def write_to_good_file(self, dir_name, filename, row):
        if filename not in self.files_names:
            raise RuntimeError("writing to unexpected file")

        if dir_name not in self.writers.keys():
            self.writers[dir_name] = {}
            os.mkdir(dir_name)

        if filename not in self.writers[dir_name].keys():
            writer = None

            full_filename = os.path.join(dir_name, filename)
            file = open(full_filename, 'w', encoding="utf-8")
            self.open_files.append(file)

            if filename == self.public_features_filename:
                writer = csv.DictWriter(file, public_field_names, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n")
            elif filename == self.all_features_filename:
                writer = csv.DictWriter(file, all_field_names, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n")
            elif filename == self.bad_records_filename:
                writer = csv.DictWriter(file, all_field_names, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n")

            writer.writeheader()
            self.writers[dir_name][filename] = writer

        self.writers[dir_name][filename].writerow(row)

    def get_folders(self):
        return self.writers.keys()