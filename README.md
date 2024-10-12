
#
stage-to-entity process execution Algorith
temp_mapping_file=$(mktemp) # Create a temporary file for the stage-to-entity mapping awk -F', tolower ($3) == "neo4j" && tolower ($4) == "y" {print $2, $1}' "$iam_stage"
304j" 8& tolower (54) - y" (print 32, sto nEtan tapen | sort -n -k1,1 - 2,2 "Stemp mapping file Fsorting active Features based on stores
| sort -n -k1,1 -k2,2 › "$temp_mapping_file"
#sorting active features based on stages
# Define a function to extract values from a YAML configuration file
extract_config_values) t
local feature_configfile="$1"
local feature_name-"$2"
# Parse the YAML configuration file
eval "$（python - ＜<END
import yaml
with open ('$feature_configfile', 'r') as file:
config = yaml.load(file, Loader=yaml. FullLoader)
batched - config-get ('$feature_name', {}) -get('batched')
print (f'batched={batched}' )
END
# Process entities in the desired order
previous_stage="* current _stage=".
total_entities=$(wc -1 < "$temp _mapping_file")
