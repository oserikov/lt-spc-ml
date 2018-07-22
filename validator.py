from tools.utils import read_csv_dict
from tools.csv_fields_names import predicted_field_names


def group_contains_predictions_selected_by_user(group):
    group_does_not_contain_any_predictions_selected_by_user = True
    for row in group:
        if bool(row["selected_by_user"]):
            group_does_not_contain_any_predictions_selected_by_user = False
    return not group_does_not_contain_any_predictions_selected_by_user


def score_predictions(filename):
    groups = {}
    for features_row_dict in read_csv_dict(filename, predicted_field_names):
        if features_row_dict["id"] in groups:
            groups[features_row_dict["id"]].append(features_row_dict)
        else:
            groups[features_row_dict["id"]] = [features_row_dict]

    model_prediction_is_right = 0
    number_of_relevant_groups_processed = 0
    for group in groups.values():
        if not group_contains_predictions_selected_by_user(group):
            continue

        number_of_relevant_groups_processed += 1

        suggestions_ordered_by_predicted_proba_desc = sorted(group, key=lambda row: float(row["proba"]), reverse=True)
        most_probable_suggestion = suggestions_ordered_by_predicted_proba_desc[0]
        if bool(most_probable_suggestion["selected_by_user"]):
            model_prediction_is_right += 1

    return float(model_prediction_is_right) / number_of_relevant_groups_processed

if __name__ == '__main__':
    print(score_predictions(r"/ssd_data/lt/features_splitted/GERMAN_SPELLER_RULE/predicted_val.csv"))

