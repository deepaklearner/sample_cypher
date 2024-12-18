# Initializing variables

iam_stage=$(cat $project_configfile | grep -w "iam_stage" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

error_log_location=$log_location/errors/
feature_log_location=$log_location/features/
stat_log_location=$log_location/stats/

techops_log_location=$(cat $project_configfile | grep -w "techops_log_location" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

timeout_duration=$(cat $project_configfile | grep -w "timeout_duration" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

db_credentials_file=$(cat $project_configfile | grep -w "db_credentials_file" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')



In my unix script:
project_configfile='./config/INT5043_INT5353_config-yaml'
activate_file=$(cat $project_configfile | grep -w "venv_location" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

if [ -f "$activate_file" ]; then
    source "$activate_file"
else
    exit 1
fi

