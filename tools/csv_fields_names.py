all_field_names = ["id",
                   "left_context_covered", "left_context_covered_length", "left_context_covered_proba",
                   "right_context_covered", "right_context_covered_length", "right_context_covered_proba",
                   "left_context_correction", "left_context_correction_length", "left_context_correction_proba",
                   "right_context_correction", "right_context_correction_length", "right_context_correction_proba",
                   "covered", "corrected",
                   "first_letter_matches", "edit_distance",
                   "selected_by_user",
                   "rule_id", "language"]
original_field_names = [field_name for field_name in all_field_names if field_name != "id"]
private_field_names = ["left_context_covered", "right_context_covered", "left_context_correction",
                       "right_context_correction", "covered", "corrected", "rule_id", "language"]
public_field_names = [field_name for field_name in all_field_names if field_name not in private_field_names]
predicted_field_names = public_field_names + ["proba"]
