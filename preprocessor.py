from tools.csv_fields_names import original_field_names, public_field_names
from tools.file_util import FileUtil
from tools.utils import read_csv_dict, sub_dict


# noinspection PyBroadException
def preprocess(input_data_filename, all_features_filename, public_features_filename, bad_records_filename):
    previous_covered = None
    cur_id = 0
    with FileUtil(all_features_filename, public_features_filename, bad_records_filename) as file_util:
        for features_row_dict in read_csv_dict(input_data_filename, original_field_names):
            try:
                if features_row_dict["covered"] != previous_covered:
                    previous_covered = features_row_dict["covered"]
                    cur_id += 1

                features_row_dict["id"] = cur_id

                features_row_dict["left_context_covered_proba"] = float(features_row_dict["left_context_covered_proba"])
                features_row_dict["right_context_covered_proba"] = float(features_row_dict["right_context_covered_proba"])
                features_row_dict["left_context_correction_proba"] = float(features_row_dict["left_context_correction_proba"])
                features_row_dict["right_context_correction_proba"] = float(features_row_dict["right_context_correction_proba"])

                features_row_dict["left_context_covered_length"] = int(features_row_dict["left_context_covered_length"])
                features_row_dict["right_context_covered_length"] = int(features_row_dict["right_context_covered_length"])
                features_row_dict["left_context_correction_length"] = int(features_row_dict["left_context_correction_length"])
                features_row_dict["right_context_correction_length"] = int(features_row_dict["right_context_correction_length"])

                features_row_dict["edit_distance"] = int(features_row_dict["edit_distance"])

                features_row_dict["first_letter_matches"] = 1 if features_row_dict["first_letter_matches"] == 'true' else 0
                features_row_dict["selected_by_user"] = int(features_row_dict["selected_by_user"])

                file_util.write_to_good_file(features_row_dict["rule_id"], public_features_filename, sub_dict(features_row_dict, public_field_names))
                file_util.write_to_good_file(features_row_dict["rule_id"], all_features_filename, features_row_dict)

            except Exception:
                file_util.write_to_good_file(features_row_dict["rule_id"], bad_records_filename, features_row_dict)

        return file_util.get_folders()


if __name__ == '__main__':
    preprocess(r"C:\Users\olegs\Documents\features22processed.headless.csv", "all.csv", "public.csv", "bad.csv")
