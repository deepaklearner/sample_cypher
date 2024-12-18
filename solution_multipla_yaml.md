#!/bin/bash

# Path to the YAML configuration file
project_configfile='./config/supervisor_hierarchy_config.yaml'

# Extracting values for supervisor_hierarchy_report_ProjConfig
report_log_location=$(awk '/^supervisor_hierarchy_report_ProjConfig:/,/^supervisor_hierarchy_ProjConfig:/' $project_configfile | grep -w "log_location" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
report_batch_size=$(awk '/^supervisor_hierarchy_report_ProjConfig:/,/^supervisor_hierarchy_ProjConfig:/' $project_configfile | grep -w "batch_size" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
report_timeout_duration=$(awk '/^supervisor_hierarchy_report_ProjConfig:/,/^supervisor_hierarchy_ProjConfig:/' $project_configfile | grep -w "timeout_duration" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

# Extracting values for supervisor_hierarchy_ProjConfig
supervisor_log_location=$(awk '/^supervisor_hierarchy_ProjConfig:/,/^$/' $project_configfile | grep -w "log_location" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
supervisor_notification_log_location=$(awk '/^supervisor_hierarchy_ProjConfig:/,/^$/' $project_configfile | grep -w "notification_log_location" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
supervisor_timeout_duration=$(awk '/^supervisor_hierarchy_ProjConfig:/,/^$/' $project_configfile | grep -w "timeout_duration" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
supervisor_batch_size=$(awk '/^supervisor_hierarchy_ProjConfig:/,/^$/' $project_configfile | grep -w "batch_size" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

# Print variables (optional for debugging)
echo "Report Log Location: $report_log_location"
echo "Report Batch Size: $report_batch_size"
echo "Report Timeout Duration: $report_timeout_duration"

echo "Supervisor Log Location: $supervisor_log_location"
echo "Supervisor Notification Log Location: $supervisor_notification_log_location"
echo "Supervisor Timeout Duration: $supervisor_timeout_duration"
echo "Supervisor Batch Size: $supervisor_batch_size"
