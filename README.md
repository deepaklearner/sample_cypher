import pandas as pd import numpy as np import warnings import logging
#Interim Data transformation
def fetch_int _workday_data(data_frame):
This function will generate below columns:
1. is new _hire
2. date_current
3. startDate
This will also convert datatype as string for whole dataframe
..
def priority_cols(row):
row=row[row!=pd.NaT]
return row[O] if row.size else "DNE"
warnings. simplefilter(action=' ignore', category=pd. errors PerformanceWarning)
data_frame.values[pd. isna(data_frame.values)]='DNE'
df = date _parser_category_one(data_frame)
df ['source']=' INT5043'
def process_data mapping(data_mapping:dict, df:pd.DataFrame) :
data_mapping: it is feature wise data_mapping
numpy methods: 330 ms + 8.22 ms per loop (mean + std. dev. of 7 runs, 1 loop each) lambda methods: 3.25 s $ 30.9 ms per 100p (mean ‡ std. dev. of 7 runs, 1 loop each)
def priority_cols(row):
row=row[row!= 'DNE']
return row[0] if row.size else "DNE"
if data _mappingl'priority_cols'] is not None:
#logging-info(f"data_mapping-
-: \n {data_mapping}")
for i in data_mapping['priority_cols']:
x = data mapping[ priority_cols'][1] split(*,*)
df[1] - np-apply_along_axis(priority_cols,axis=1,arr=df[x] .values)
if data _mapping['is_y_n_cols'] is not None:
for & F ata napine 1sycols 11).sit(';)
if x[0] == 'DNE':
df［i］='N'
else:
df[1]-np-where((df[x] != "DNE" ) -any (axis=1), Y•, N°)
if data_mapping[ concat_attr_cols'] is not None: for i in data_mapping[ concat_attr_cols']:
x = data_ mapping[ concat_attr_cols'][i].split(')
df [i]-list(map("* - join,np.array(df[x])))
return df
def date_parser_category_one(df):
# Convert date columns to datetime format with error coercion
for col in ['hireDate'
, 'contractstartDate']:
df. loc[df[col] == 'DNE', col] = np. nan
df [col] = pd. to_datetime(df[col], errors='coerce', utc=True)
df[col] = df[col].dt. strftime ('%Y-%m-%dT%H:%M:%5%z*). replace( 'NaT', np. nan)
df[col] = pd. to_datetime(df[col], errors='coerce').dt.tz_localize(None)

# Define current date
current_date = pd. Timestamp.now()
future_date = '2099-01-04'
#To be handled
condition1 = df[['hireDate',
'contractstartDate']].bfill(axis=1).iloc[:, 0]-ge(current_date)
df['date_current'] = np.where(condition1,
dfI[ 'hireDate', 'contractstartDate' ]].bfill(axis=1). iloc[:, 0],
current_ date)
df['date_current'] = df['date_current']. fillna (current date)
df['date_current ']=pd. to datetime(df['date_current ']).dt.tz localize(None)
df ['startDate'] = np.where(condition1,
af|['hireDate', 'contractstartDate']].bfill(axis=1).iloc[:, 0],
pd. to_datetime (future_date))
df['startDate'] = df['startDate']. fillna(pd. to datetime(future_date))
df['startDate ']=pd.to_datetime(df['startDate']).dt.tz_localize(None)
df = df. astype(str)
df = df. replace(r' 2099-01-04', 'DNE', regex=True)
#Condition for NewHire Flag
condition2 = df['employmentStatus'] == 'A'
condition3=
df ['userType'] != 'DNE'
d['is _new _hire']= np. where(condition & condition2 & condition, 'Y', 'N')
return df
def date_parser_category_twodf,driving_dt_col, feature_name) :
# Convert date columns to datetime format with error coercion
for col in ['hireDate'
, driving_dt_col,
'contractstartDate']:
df. loc[df[col] == 'DNE', col] = np. nan
df [col] - pd. to _datetimedf[col], errors= 'coerce', utc-True)
df[col] = df[col].dt.strftime (%Y-%m-%dT%H:%M:%5%z*). replace(NaT', np. nan)
df [col] = pd. to_datetimedf[col], errors='coerce') .dt.tz_localize(None)
# Define current date
current_date - pd. Timestamp. now()
future_date - 2099-01-04*
#To be handled
# Create conditions based on the SQL query
condition1 = df[['hireDate',
•contractstartDate']].bfill(axis=1).iloc[:, 0].ge(current_date)
condition2 = df[driving_dt_col]-notna)
# Apply conditions to create new column
df [f'date_{feature_name)*] - np.wherecondition,
df[[driving_dt_col, hireDate',
*contractstartDate ]].bfill(axis=1).iloc|:, 0],
np.where(condition2, df[driving_dt_col], current _date))
df[f date_{feature_name} '] - df[f'date_{feature_name}']. fillna(current_date)
df[f'date_(feature_name) ']pd. to _datetime(df[f'date_{feature_name}']).dt.tz_localize(None)
df[f'startDate_(feature_name}'] = np.where(condition,
df[[driving_dt_col,
hireDate',
* contractstartDate ]].bfill(axis=1).iloc:, 0],
np.where(condition2, df[driving_dt_col], pd. to _datetime(future_date)))
df[f'startDate_{feature_name}'] = f[f'startDate_{feature_name}'].fillna(pd. to datetime(future_date))
df[f'startDate_(feature_name}'l=pd. to_datetime(df[f'startDate_{feature_name} ']).dt.tz_localize(None)
df = df.astype(str)
df - df. replace(r' 2099-01-04*, 'DNE', regex=True)
return df
def extract_employeeTypeStatus(df, is_future_EmployeeType_required='N'):
conditions_current = [ (df['userType'] == 'Employee'),
(df['userType'] == 'Contractor'), (df['userType'] == 'Vendor')
values - ['E', C', v]
df ['CurrentEmployeeType']= np.select(conditions_current, values, default='DNE*


if is_ future_EmployeeType_required==*Y*:
conditions_ future = [
(df[' cfFutureIdentityType']=='Employee'),
(df[' cfFutureIdentityType']=='Contractor')
(df ['cfFutureIdentityType'] ==
'Vendor")
]
df[ 'FutureEmployeeType ]= np. select(conditions_future, values,default ='DNE')
return df
def first_non_null (arr, current_date) -› np.datetime64: return p.datetime64(next(filter(lambda i: not
np. isnan(i), arr), current _date))
#Feature Specific Data transformation
#-
def data_manipulation User(data mapping:dict, df:pd DataFrame):
df= process_data_mapping(data_mapping, df)
df = extract_employeeTypeStatus (df, 'N*)
df['userProfileID'] = 123456'
df['aetnaNetworkID'] = *123456*
df['cvsNetworkID'] = 123456'
d['eligibilityCode'] = *123456'
df[ EmployeeType '] = df[ 'CurrentEmployeeType']
# df. to_csv('data-manipulation.csv,index=False)
return df

def data_manipulation_GenericAttributeFeature(data mapping:dict, df:pd. DataFrame):
df - process _data mapping(data mapping, df)
return df

def data_manipulation JobFeature(data mapping:dict, df:pd. DataFrame) :
df = process_data _mapping(data_mapping, df)
df[ jobLevelDescription']='ToBeDecided #Need to discuss with Murali
return df

def data_manipulation PayFeature(data _mapping:dict, df:pd. DataFrame):
df = process_ data_mapping(data_mapping,df)
return df
def data_manipulation_ VendorFeature(data mapping:dict, df:pd .DataFrame) :
df = process _data_mapping(data mapping, df)
df| " vendorName'] = ToBeDecided #Discuss with Murali
return df
def data manipulation EmailFeature(data mapping:dict, df:pd.DataFrame):
df = process_data mapping (data_mapping,df)
conditions = [
(df[ 'EmailHome']!= 'DNE'),
(df ['EmailHome '] == 'DNE') & (df[' cfContractorPersonalEmail] != 'DNE*)
choices = [
df['EmailHome',
df [ 'cfContractorPersonalEmail']
df[ output'] = np. select (conditions, choices,
default="DNE*)
df[[' employeeNumber', ' EmailHome',
'cfContractorPersonalEmail', 'output']]
return df
def data manipulation NameFeature(data_mapping:dict, df:pd.DataFrame):
df = process _data _mapping(data_mapping, df)
df['concat_attr_PreferredName'] = list (map (
lambda x:
-join(filter(None, x)),
zip(
np.where(df.prefPrefix == 'DNE','',df.prePrefix),
np.where(df .prefFirstName == 'DNE', '',df.prefPrefix),
p. where(df prefMiddleName == 'DNE','', df. prefFirstName),
np.where(df.prefLastName== 'DNE','', df.preMiddleName.str[0]),
, df. prefLastName)
)

))


df['is_PreferredName '] = np. where(df['concat_attr_PreferredName*]==**, N*,*Y*)
df[' concat_attr_Name']=list(map(lambda x: • -join(filter(None, x)),
zip(np.where(df.honorificPrefix =='DNE','',
, df.honorificPrefix),
np. where(df. givenName == 'DNE',
, df. givenName),
np.where(df.middleName == 'DNE','',
df.middleName.str [0]), np.where(df.familyName == 'DNE', '', df. familyName))))
dfL'is_Name'] = np.where(df['concat_attr_Name']=='', 'N', 'Y*)
df[ 'honorificSuffix']=df[ 'lastnamesuffix'] #This will change
return df

def data manipulation AddressFeature(data_mapping dict, df :pd.DataFrame) :
df = process_data_mapping(data_mapping, df)
df[' concat_attr_HomeAddress']=list(map(
lambda x:' '.join(filter((None,x)),

zip(
np.where df. HomestreetAddress == *DNE*,
, df. HomestreetAddress),
np. where(df.Homelocality == 'DNE*
, df. Homelocality),
np. where(df. Homeregion == 'DNE'
df. Homeregion),
np. where (df.HomepostalCode == 'DNE'
.: df. HomepostalCode),
p. where (df. prefCountryCode == 'DNE', , df.prefCountryCode)
)
))
afl concat_attr _WorkAddress'] = list(map (
lambda x: • • join (filter(None, x)), zip(
p-where df WorkstreetAddress == 'DNE*,*, df. WorkstreetAddress), np. where(df.worklocality == 'DNE'
p. where(df. workregion = "DNE", !.
, df.worklocality),
, df. workregion),
np.where(df.workpostalCode
'DNE',', df.workpostalCode),
p. where(df.workcountry == 'DNE',", df.workcountry)
aflis HomeAddress'] = p.where(df['concat_attr_HomeAddress' ]==*
df['is WorkAddress'] = np.where(df['concat_attr_WorkAddress*]-*
•NUY
return df

def data_manipulation_ PhoneFeature(data_mapping: dict, df: pd.DataFrame) :
df= process_data_mapping (data_mapping,df)
dfI'isTempProperty']=*Y'
df[ defaultcode']=DNE* #Need to check with Murali in case of workphone for code return df
def data manipulation_IdentificationAndAccessData(data_mapping:dict, df:pd.DataFrame):
df = process_data_mapping(data_mapping, df)
return df

def data_manipulation_CVSIdentifier(data_mapping:dict, df:pd.DataFrame) :
assignment_rules = data _mappingl'cid_assignment_rule']
df = df[df['employmentStatus']=='A']
warnings. simplefilter(action='ignore')
df ['jobCode'] = df[' jobCode']. str.split('.').str[0]
combined_filter = None
for i in assignment_rules:
filtered_val = None
for key, val in i.items ():
df [key] = df[key].str.upper()
if filtered_val is None:
filtered_val = (df[key] isin(val))
else:
filtered_val &= (df[key]. isin(val))
if combined filter is None:
combined_filter - filtered_val else:
combined_filter | = filtered_val
df = df[combined_ filter]
df = df.astype(str)
return df

def data_manipulation Aetnaldentifier(data_mapping:dict, df:pd.DataFrame)

assignment_rules =data_mapping['aid_assignment_rule']

df = df[df['employmentStatus ']=='A']
warnings. simplefilter(action='ignore')
d['organizationId'] = df[ 'organizationId']. str split('-').str[0]
combined filter = None
for i in assignment_rules:
filtered_val = None
for key,val in i. items (:
df [key] = df[key]-str.upper ()
if filtered val is None:
filtered _val = (df[key]. isin(val))
else:
filtered _val &= (df[key]. isin (val))
if combined_filter is None:
combined_filter = filtered_val
else:
combined_filter |= filtered_val
df = df[combined_filter]
df = df.astype(str)
return df
def
data_manipulation_ConversionIdentifier(data_mapping:dict, df:pd.DataFrame) :
df = df[df[employmentStatus ']--'A']
return df
#-> Info Nodes call for category
def data manipulation_CostCenterInfo(data_mapping:dict, df:pd.DataFrame) :
df = process_data_mapping(data_mapping,df)
df [* FutureCostCenterName'] = *DNE*
return df
def data_manipulation UserTypeInfo(data_mapping:dict, df:pd.DataFrame):
df =
process
data_mapping(data _mapping, df)
df = extract_employeeTypeStatus (df, 'Y*)
return df
def data_manipulation_OrganizationInfo(data_mapping:dict, df:pd.DataFrame):
df = process_data_mapping(data_mapping, df)
return df
def data_manipulation DivisionInfo(data_mapping:dict, df:pd.DataFrame):
df=Process-data_mapping(data_mapping, df)
conditions current = L (df['division'] = *AETNA*),
(df['division'] == *HEADQ*),
(df[ 'division']
-= "STORE*),
(df['division] == *RXSRV*),
(df['division'] -= *DISTR'),
(df['division']
- CMARK'),
(df[ division] == *CMRTL*),
(df[ division']
== 'MINPC"),
(df|'division']
(df['division' ] == VENDR*),
]
conditions_future
= [ (df[' cfFutureDivision] - AETNA*),
(df['cfFutureDivision]
"HEADQ"),
(df[' cfFutureDivision']
- 'STORE'),
(df['cfFutureDivision']
(df[ 'cfFutureDivision']
(df[' cfFutureDivision']
(df[' cfFutureDivision']
(df[' cfFutureDivision']
DISTR'),
' CMARK"),
* CMRTL*),
" MINPC'),
(df['cfFutureDivision']
(df[ 'cfFutureDivision']
= VENDR'),]

values = [
'Aetna',
'Corporate Offices',
'Stores'
"Pharmacy',
•Distribution Centers',
' Caremark',
'Caremark Retail',
'MinuteClinic',
'MinuteClinic LLC',
"Vendor'
df[ current_division_name']= np. select(conditions_ current, values, default = 'DNE*)
df['future _division _name']= np. select(conditions_ future, values, default=*DNE*) return df
def data_manipulation_ JobLocationInfo(data_mapping:dict, df:pd.DataFrame):
df - process_data_mapping (data_mapping,df)
df[ 'FuturelocationName ']=df['FuturelocationType']=df['FutureteleworkModel *]=df['FuturesupportLocation ]= DNE
df[ 'supportLocation']= DNE'
return df
-> Info Nodes call for category2
def data manipulation_UserJobInfo(data_mapping:dict, df:pd.DataFrame) :
try:
df - process_data_mapping(data_mapping,df)
df-date_parser_category_twodf, 'cfJobChangeEffectiveDate, UserJobInfo*)
except Exception as e:
logging. error (e)
return df
def data manipulation ProfileStatusInfo(data_mapping:dict, df:pd.DataFrame):
try:
df = process_data_mapping(data_mapping, df)
df = date_parser _category_twodf, 'cfEmploymentStatusEffectiveDate', 'profilestatusinfo')
except Exception as e:
logging. error (e)
return df
def data manipulation Department_hierarchy(data_mapping:dict,
df: pd.DataFrame):
df = pd.mergedf ,df.dropna(subset=['Sup_Org_ID*]), left_on="superiorOrgID', right_on= Sup_Org_ID* ,
how='left'
, suffixes=('_current', _parent*))
df = df. fillna( 'DNE')
return df
def data_manipulation_Department(data_mapping:dict, df:pd.DataFrame):
df = process_data_mapping(data_mapping, df)
df = date_parser_category_twodf, 'departmentEffectiveDate', 'deptinfo')
return df
# -> PostProcessing call
def data manipulation PostProcessing(data_mapping:dict, df:pd.DataFrame):
df = pd. DataFrame()
return df
def data manipulation_PostProcessing_EDW(data_mapping:dict, df:pd .DataFrame):
df=pd.DataFrame()
return df


