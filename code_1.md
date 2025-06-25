def validate_employee_data(data_frame, config_file):
    def check_rejections(df):
        # Mask: Rows where contractor label exists
        has_contractor_label = df['labels'].apply(lambda labels: 'Contractor' in labels)

        # Mask: Rows where conversionType is NOT 'c2e' in feed file
        is_not_conversion = df['conversionType'].str.lower() != 'c2e'

        # Filter
        incorrect_record_type = df[has_contractor_label & is_not_conversion]
        reject_record_type_df = incorrect_record_type[['employeeNumber']].copy()
        reject_record_type_df['Reason'] = "conversion type is not c2e in iamids_adhoc_conversion feed"

        # Mask: Labels do NOT contain 'Active' or 'OnLeave'
        missing_active_onleave_label = ~df['labels'].apply(
            lambda labels: any(l in ['Active', 'OnLeave'] for l in labels)
        )

        # Filter
        reject_employment_status_df = df[missing_active_onleave_label]
        reject_employment_status_df['Reason'] = (
            "User type change detected. employmentStatus in ['A', 'L'] but missing 'Active'/'OnLeave' label in Neo4j"
        )

        # Combine mismatches
        combine_mismatches = pd.concat([reject_record_type_df, reject_employment_status_df], ignore_index=True)

        # Group by employeeNumber and aggregate reasons
        mismatch_df = combine_mismatches.groupby('employeeNumber')['Reason'].agg('; '.join).reset_index()

        return mismatch_df

    # Example usage inside validate_employee_data:
    return check_rejections(data_frame)
