import pandas as pd
import numpy as np


#loading the data:
print("loading the data ...")
df = pd.read_csv("Flights_raw_data.csv")
print("raw data loaded !")



#data profiling, giving general information about the dataset like the number of null rows and duplicates
print("profiling the data...")
print("Shape (rows, columns):")
print(df.shape)

print("\nFirst 5 rows of the dataset:")
print(df.head())

print("\ninformation about the Dataset :")
df.info()

print("\nStatistical summary of the dataset:")
print(df.describe())

print("\nNumber of missing values per column:")
print(df.isnull().sum())

print("\nNumber of duplicate rows:")
print(df.duplicated().sum())

#cleaning the data : 
print("cleaning the data...")
#1-removing duplicate values
df = df.drop_duplicates()

#2-dealing with missing values
#first we seperate the numerical and categorical data types
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = df.select_dtypes(include=['object']).columns

#then we clean each type of data seperatly
df[numeric_cols] = df[numeric_cols].fillna(0)
df[categorical_cols] = df[categorical_cols].fillna('Unknown')


#3-fixing the data types
date_cols = ['FlightDate']

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

numeric_cols = df.columns.difference(date_cols)
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='ignore')

categorical_cols = df.select_dtypes(include=['object']).columns
df[categorical_cols] = df[categorical_cols].astype('category')

#dealing with outliners
def cap_outliers(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return series.clip(lower, upper)

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

exclude_cols = ['Year', 'Month', 'FlightID']
outlier_cols = [col for col in numeric_cols if col not in exclude_cols]

for col in outlier_cols:
    df[col] = cap_outliers(df[col])

#validating the cleaning and transformation of data
print("checking if the data is cleaned...")
print("shape (rows,columns) :")
print(df.shape)
print("first 5 rows of the dataset")
print(df.head())
print("Number of missing values per column:")
print(df.isnull().sum())
print("Number of duplicated rows:")
print(df.duplicated().sum())

#exporting the clean data in csv format
print("exporting the clean data...")
df.to_csv("flights_data_cleaned.csv", index=False)

#generating the data dictionary:
print("generating the data dictionary")
data_dictionary = pd.DataFrame({
    'Column Name': df.columns,
    'Data Type': df.dtypes.astype(str),
    'Description': [
            'FlightDate',                               
            'Airline',                                  
            'Origin',                                   
            'Dest',                                   
            'Cancelled',                               
            'Diverted',                                 
            'CRSDepTime',                               
            'DepTime',                                  
            'DepDelayMinutes',                          
            'DepDelay',                                 
            'ArrTime',                                  
            'ArrDelayMinutes',
            'AirTime',                          
            'CRSElapsedTime',                           
            'ActualElapsedTime',                        
            'Distance',                                 
            'Year',                                     
            'Quarter',                                  
            'Month',                                    
            'DayofMonth',                               
            'DayOfWeek',                                
            'Marketing_Airline_Network',                
            'Operated_or_Branded_Code_Share_Partners',  
            'DOT_ID_Marketing_Airline',                 
            'IATA_Code_Marketing_Airline',              
            'Flight_Number_Marketing_Airline',         
            'Operating_Airline',                        
            'DOT_ID_Operating_Airline',                
            'IATA_Code_Operating_Airline',              
            'Tail_Number',                              
            'Flight_Number_Operating_Airlin',          
            'OriginAirportID',                          
            'OriginAirportSeqID',                       
            'OriginCityMarketID',                       
            'OriginCityName',                           
            'OriginState',                              
            'OriginStateFips',                          
            'OriginStateName',                          
            'OriginWac',                                
            'DestAirportID',                            
            'DestAirportSeqID',
            'DestCityMarketID',                         
            'DestCityName',                             
            'DestState',                                
            'DestStateFips',                            
            'DestStateName',                            
            'DestWac',                                  
            'DepDel15',                                 
            'DepartureDelayGroups',                     
            'DepTimeBlk',                               
            'TaxiOut',                                  
            'WheelsOff',                                
            'WheelsOn',                                 
            'TaxiIn',                                   
            'CRSArrTime',                               
            'ArrDelay',                                 
            'ArrDel15',                                 
            'ArrivalDelayGroups',                       
            'ArrTimeBlk',                               
            'DistanceGroup',                            
            'DivAirportLandings',                   
    ]
})

data_dictionary.to_csv("data_dictionary.csv", index=False)
