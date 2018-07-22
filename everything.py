import os

from data_shuffle_splitter import split_original_csv_to_train_test_val_csv
from ml import ml
from preprocessor import preprocess
from validator import score_predictions

input_lt_data = r"/ssd_data/lt/features_processed.csv.headless"
all_features_filename = "all.csv"
public_features_filename = "public.csv"
bad_records_filename = "bad.csv"
train_data_filename = "train.csv"
test_data_filename = "test.csv"
val_data_filename = "val.csv"
output_model_filename = "xgb.model"


if __name__ == '__main__':
    folders = preprocess(input_lt_data, all_features_filename, public_features_filename, bad_records_filename)
    for f in folders:
        train_data_full_filename = os.path.join(f, train_data_filename)
        test_data_full_filename = os.path.join(f, test_data_filename)
        val_data_full_filename = os.path.join(f, val_data_filename)
        predicted_val_data_full_filename = os.path.join(f, "predicted_" + val_data_filename)
        output_model_full_filename = os.path.join(f, output_model_filename)
        print("before split for folder " + f)
        split_original_csv_to_train_test_val_csv(os.path.join(f, public_features_filename),
                                                 original_data_csv_headless=False,
                                                 train_data_filename=train_data_full_filename,
                                                 test_data_filename=test_data_full_filename,
                                                 val_data_filename=val_data_full_filename)
        print("before ml for folder " + f)
        ml(train_data_full_filename, val_data_full_filename, predicted_val_data_full_filename, output_model_full_filename,
           first_column_id=True)
        print(predicted_val_data_full_filename)
        print(f + "\t" + str(score_predictions(predicted_val_data_full_filename)))
