#!/bin/bash
# Script: generate_supervisor_hierarchy_report.sh
# Author: TCS IAM BuildTeam
# Version: 1.0
# Description:
# Init Process
if L -z "$1" ];then
cd /opt/cvs/Ne04J_Inbound/pipeline_routines/supervisor_hierarchy #Default Working Directory in case if no argument is passed
else
cd "$1"
fi
start_time=$(date +*%Y-%m-%d %H:%M: %5*)
project_ configfile=/opt/cvs/Utils/config/pipeline_routines/supervisor_hierarchy/config.yaml'
activate_ file=$(cat Sproject_configfile | grep -w
# /config/config-yaml
"venv_location"
cut
-d
-f2 | sed 's/^[[:space: ]1*//g')
# Check if activate file exists
if [ -f "Sactivate_file" ]:
then
# Activate the virtual environment
source
"Sactivate_file"
echo "Virtual environment activated."
else
echo
"Error: Virtual environment not found or activate file does not exist."
exit 1
fi
# Function written to handle Interrupt Signal
cleanup_functionOU
echo "Interrupt signal received, Stopping backend python process....
program_user-" whoami
ghp_M2WD4vqUaRf1Fbpj9sL5zPA@hRb5iA3wt6kx, last week • d
pkill
-u Sprogram user python
exit 1
trap cleanup_function SIGINT
# Initializing variables for supervisor_hierarchy_ProjConfig
main_log_ history_days=$(cat Sproject_configfile |
grep -w "main_log_history_days" | cut -d ':' -f2 | sed *s/^[[:space:]]*//g*)
error_log_history_days=$(cat Sproject_configfile
grep -w "error_log_history_days"
cut -d
-f2 | sed *s/^[[: space:]1*//g')
stat_log_history_days-$(cat $project_configfile 1
grep -w "stat_log_history_days"
| cut -d ':' -f2 | sed 's/^[[:space:]]*//g')
log location=$(awk
•/supervisor_hierarchy_report_ProjConfig:/,/^$/' Sproject_configfile | grep -w "log_location" | cut -d ':* -f2 | sed *s/^[[: space: ]]*//g')
error_log_location=$10g_location/errors/ stat log location-$log location/stats/
timeout _duration-$(cat Sproject_configfile | grep -w "timeout_duration" | cut -d ':' -f2 | sed *s/^[[: space: ]]*//g')
mkdir -p flog location mkdir
-p Serror_log location mkdir -p $stat_10g location

#remove error logs directory find $log_location -maxdepth 1
-mtime +$main_log_history_days -type f -name "*. 10g"
find ferror_log location -maxdepth 1-mtime +$error_log history_days -type f -name
-delete
"*.10g"
find $stat_log_location -maxdepth 1-mtime +$stat_log history _days -type f -name "*.10g"
-delete
-delete
10g_ file="$log_location/generate_ supervisor_hierarchy_report_$(date +"%Y-%m-%d_%T"). log*
echo "$(date +"%Y-%m%d %T"): $1" » "$log_file*
cd ../supervisor_hierarchy/
python -B generate_supervisor_hierarchy_report-py --log_location=$log location>> "$log_file" 2>&1
# Update Stats for Timeout feature
timedout_ feature= cat $10g_file | grep
"Process Timed Out for" | rev | cut -d = •
-f1 | rev*
for i in $timedout_ feature do
echo $i
sed -i "/$i,/d" $stat_file
echo "$i， "Timeout”， N" >> $stat_file
done
# Calculate the duration
end_time-$(date +"%Y-%m-%d %H:%M:%5")
start_seconds=$(date -d "$start_time" +%s)
end_seconds=$(date -d "$end_time"
+%5)
duration=$((end_seconds - start_seconds))
# Displaying the captured times and duration
echo "Start Time: $start_time" echo
"End Time: $end_time"
echo "Generate supervisor hierarchy report job completed in $duration seconds. Please Debug stats & Logs for exact status!!" log "Generate supervisor hierarchy report job completed in $duration seconds. Please Debug stats & Logs for exact status!!"


