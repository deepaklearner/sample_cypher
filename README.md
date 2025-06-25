1.1 In below code, please replace below logic, by terminated_label and reject_employment_status_df
where "Termiated" label is present instead of checking if "Active" or "OnLeave" missing

"""
missing_active_onleave_label = ~df['labels'].apply(
            lambda labels: any(l in ['Active', 'OnLeave'] for l in labels)
        )
reject_employment_status_df = df[missing_active_onleave_label]"""