#!/bin/bash
# Script: generate_supervisor_hierarchy_report.sh
# Author: TCS IAM BuildTeam
# Version: 1.0
# Description: This script generates the supervisor hierarchy report.

# Init Process
if [ -z "$1" ]; then
  cd /opt/cvs/Neo4J_Inbound/pipeline_routines/supervisor_hierarchy  # Default Working Directory if no argument is passed
else
  cd "$1"
fi

start_time=$(date +"%Y-%m-%d %H:%M:%S")

project_configfile="/opt/cvs/Utils/config/pipeline_routines/supervisor_hierarchy/config.yaml"
activate_file=$(cat "$project_configfile" | grep -w "venv_location" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

# Check if activate file exists
if [ -f "$activate_file" ]; then
  # Activate the virtual environment
  source "$activate_file"
  echo "Virtual environment activated."
else
  echo "Error: Virtual environment not found or activate file does not exist."
  exit 1
fi

# Function written to handle Interrupt Signal
cleanup_function() {
  echo "Interrupt signal received, Stopping backend python process..."
  program_user=$(whoami)
  pkill -u "$program_user" python
  exit 1
}
trap cleanup_function SIGINT

# Initializing variables from supervisor_hierarchy_ProjConfig
main_log_history_days=$(cat "$project_configfile" | grep -w "main_log_history_days" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
error_log_history_days=$(cat "$project_configfile" | grep -w "error_log_history_days" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
stat_log_history_days=$(cat "$project_configfile" | grep -w "stat_log_history_days" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
log_location=$(awk '/supervisor_hierarchy_report_ProjConfig:/, /^$/' "$project_configfile" | grep -w "log_location" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
error_log_location="$log_location/errors/"
stat_log_location="$log_location/stats/"
timeout_duration=$(cat "$project_configfile" | grep -w "timeout_duration" | cut -d ':' -f2 | sed 's/^[[:space:]]*//g')

# Create necessary directories
mkdir -p "$log_location"
mkdir -p "$error_log_location"
mkdir -p "$stat_log_location"

# Remove old log files
find "$log_location" -maxdepth 1 -mtime +$main_log_history_days -type f -name "*.10g" -delete
find "$error_log_location" -maxdepth 1 -mtime +$error_log_history_days -type f -name "*.10g" -delete
find "$stat_log_location" -maxdepth 1 -mtime +$stat_log_history_days -type f -name "*.10g" -delete

# Generate report
log_file="$log_location/generate_supervisor_hierarchy_report_$(date +"%Y-%m-%d_%T").log"
echo "$(date +"%Y-%m-%d %T"): $1" >> "$log_file"

cd ../supervisor_hierarchy/
python -B generate_supervisor_hierarchy_report.py --log_location="$log_location" >> "$log_file" 2>&1

# Update Stats for Timeout feature
timedout_feature=$(cat "$log_file" | grep "Process Timed Out for" | rev | cut -d '=' -f1 | rev)

for i in $timedout_feature; do
  echo "$i"
  sed -i "/$i,/d" "$stat_log_location"
  echo "$i, Timeout" >> "$stat_log_location"
done

# Calculate the duration
end_time=$(date +"%Y-%m-%d %H:%M:%S")
start_seconds=$(date -d "$start_time" +%s)
end_seconds=$(date -d "$end_time" +%s)
duration=$((end_seconds - start_seconds))

# Displaying the captured times and duration
echo "Start Time: $start_time"
echo "End Time: $end_time"
echo "Generate supervisor hierarchy report job completed in $duration seconds. Please Debug stats & Logs for exact status!" >> "$log_file"
