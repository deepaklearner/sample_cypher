1.1 In below code, please replace below logic, by terminated_label and reject_employment_status_df
where "Termiated" label is present instead of checking if "Active" or "OnLeave" missing

"""
missing_active_onleave_label = ~df['labels'].apply(
            lambda labels: any(l in ['Active', 'OnLeave'] for l in labels)
        )
reject_employment_status_df = df[missing_active_onleave_label]"""

1.2 I have a dataframe data_frame containing two columns:
employeeNumber and conversionType.

I have to apply multiple levels of validation rules:
a. Find existing user in neo4j -> If user not found write to another dataframe with Reason "User not found" 
b. If user found in neo4j -> check user node contains label OnLeave or Active else skip and write to another dataframe with Reason "User node do not contain OnLeave or Active label" 
b. Check if Employee label is present in user node label then skip saying Reason "User is already an Employee"
c. Check if Domestic label is present in User node label, else skip saying Reason "Domestic label not present" 
