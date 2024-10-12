#l/bin/bash
• Script: generate_reports.sh
# Author: TCS BuildTeam
• Description: This script creates report based on feature (report_1d) from a CV file in the desired order, running Python scripts in the background and capturing their PIDs. It displays a "running" status while processing.
# Init Process
if [ -z *$2" ]:then
cd /opt/cvs/Ne43_Inbound/REPORTS #Default Working Directory in case if no argument is passed else
cd "$2"
f
report id-$1
start time-$(date +*%Y-%m-%d %H:%M:%5*)
project_ configfile='./config/config-yaml*
activate_file-$(cat Sproject_configfile | grep -w "venv_location" | cut -d*:' -f2 | sed *s/*[[:space: ]]*//g*)
# Check if
activate file exists
if [ -f "Sactivate_file" ]: then
# Activate the virtual environment
source "Sactivate_file"
echo
"Virtual environment activated."
echo
*Error: Virtual
environment not found or activate file does not exist.-
• Function written to handle Interrupt Signal cleanup_functionot
ecto
"Interrupt signal received, Stopping backend python process....
program user- whoami
pkall -u Sprogram user python exit 1
trap cleanup_function SIGINT
* Initializing variables
lam stage=$(cat Sproject _configfile | grep -w "iam stage" | cut -d *:*
-f2 | sed "s/^[[:space: 11*//g*)
feature_configfile-$(cat project configfile | grep -w "report_feature config" | cut
-f2 1 sed's/AIl:space:11*11g）
main log history_days-$(cat Sproject_ configfile | grep -w "main_log_history_days* | cut -d *:*
f2 | sed *s/^[[:space: 11*//g*)
error_ log history_days=$(cat Sproject_configfile | grep -w "error_log_ history_days" | cut
-f2 | sed 's/^[[:space:]]*//g*)
stat_log history_days=$(cat Sproject_configfile
grep -w "stat_log_history_days"
cut -d":
-f2 | sed "s/^[[: space: ]1*//g*)
log location-$(cat Sproject configfile | grep -w "log_ location" | cut -d *:*
-f2 | sed *s/^[[:space: ]]*//g*)
error_log location-$log location/errors/ feature_log location-$10g location/features/ stat log location-$10g location/stats/
techops_log location=$(cat Sproject configfile | grep
- "techops_ log_location" | cut -d *:' -f2 | sed *s/^[[:space:11*//g*)
timeout _duration-$(cat Sproject configfile | grep -w
"timeout_duration" | cut -d
f2 | sed *s/^[[: space: 1)* //8*)
d_crendentials file-$(cat Sproject_configfile | grep -w "db_crehdentials _file" | cut -d
•: -f2 | sed 's/^[[:space:]]*//g*)

mkdir -p $log location mkdir -p $feature_ log_location
kdir -p Serror _log location kdir -p $stat log location
-p Stechops_log location
#remove feature log directory and error logs directory
rm -f $feature_1og_location
find $10g location -maxdepth 1 -mtime +Smain_log_history_days -type f -name "*. 10g"
-delete
find Serror_log location -maxdepth 1 -mtime
+Serror_10g_history_days -type f -name "*,1og"
-delete
find stat log location -maxdepth 1 -mtime +$stat_log history_days -type f -name
"*, 10g"
-delete
10g_file-"$log_location/REPORTS_$(report_id^^}_$(date +"gY-%m-%d_%T*). log*

IS>S run reportch
(date + sY-m-d sT): $1 > "Slog file"
curencely process executon Algorith
temp mapping file-$(mktemp) # Create a temporary file for the stage-to-entity mapping
tolower s3
neo4j" && tolower ($4)
"y" (print $2, $1?'
"Siam_stage"
sort -n-k11-2,2
# Define a function to extract values from a YAML configuration file
extract config values f
Jocal teacure contigtile st
Local teature name= 2°
# Parse the YAL configuration file
eval Pychon - import yami
with open steature_ configfile,
"r as file:
contig = yant.load tile, Loader=yaml.FullLoader)
batched = config get Sfeature name', -get(batched")
print (f"batched={batched})
features based on stages
# Process entities in the desired order
prey lous stage."
current stage.
total entities-$(wc-1 < "Stemp mapping file")
completed entities-
while read -r stage entity: do
it"current stage
"$stage" 1
then
if [ -n "Sprevious stage" ]
then
f
Log Processing entities in Stage stage" current stages Sstage
LOg Processing entity: Sentity"
# Call the function to extract values for the
specified feature
extract config values "$feature configfile" "Sentity"
* Access extracted values
matcheds narcher
log FeatureName: Sentity, BatchProcessing: batched)
# Run the Python script for the current entity in the background
timeout "Stimeout duration" python -B report processor.py --feature_name-Sentity --report_id-report 1d --log location»SlogLocation»
"Slog_file* 2›81 || echo "Error: Process Timed Out for S(entity)" » "$log_file" &
pid=s!
Log "PID of Sentity: Spid"
# Increment the counter for completed entities
Completed entitles-$（（completed_enttles + 1））
# Display a "running" status
echo -ne Processing: $completed entities/$total entities\r*
previous_stage="$stage"

tone < "Stenp_mapping file"
• Mait for any remaining jobs in the last stage
wait
* Clear the "running" status echo -ne -\033[2K*
• Clean up the temporary mapping file ra "Stemp_mapping_ file*
［-e
"Serror _log_location/error.log" ] && mv "Serror_log_ location/error. log"
stat_file-"Sstat_ log location "REPORT_stats_$(date +*XY-%m-%_%T"). 10g
"Serror_log location/REPORT_error_$(date +"%Y-%m-%d_%T*).10g*
echo
turelame, Timetaken, Status › Sstat file
for file in feature_log location*;
if [ -f $file 1:
then
fname-echo $file | awk -F "feature-'
*(print $2}" | cut -d *
ftime- grep
"Overall time taken by the feature'
if cat
"Sfile"| grep -iq "ERROR" $file; then
else
fstatus=*Y'
echo "Sname", "$ftime", "$fstatus" »*
"stat_file"
= Updare stacs for neout teacure timedout feature- cat Slog file 1 grep
"Process Timed Out for" | rev | cut -d - - -f1 | rev*
for i in Stimedout feature
echo Si
sed -i /Si,/d $stat file echo "$i, "TimeOut",N° » $stat_file
# Caoture Warnings
and sending them to techops team
if grep -q WARNING" "$log_ file"; then
grep
"WARNING"
"Slog_file" › Stechops 108 location/$(basename "Slog_file")
python -B src/utils/techops load alert-py Slog_file
# Calculate the duration
end time-$(date +*XY-%m-%d %H: %M:%S*)
start seconds-$(date -d "Sstart_time" +%s)
end seconds-$(date -d "Send_time" +%s) duration-$((end_seconds - start seconds))
Displaying the captured times and duration
"Start Time: Sstart_time"
echo "End Time: Send_time"
echo REPORT Jobs completed in Suration seconds. Please Debug stats & Logs for exact status!!* log "REPORT Jobs completed in Sduration seconds. Please Debug stats & Logs for exact status!!"


