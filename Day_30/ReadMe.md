## Day 30: Building Robust Data Pipelines for Washington DC Service Calls Request: End to End Data Engineering Project

🚀 After few weeks off, I am very excited to share my latest project, where I worked on Washington DC Service calls for the month of October. 
The objective of this project was to design an end-to-end data engineering pipeline on Service calls request data using Python, Pandas, AWS storage services and finally create an analytics dashboard using Tableau 📈. 

![servicecall_requests](https://github.com/Sylvesterchuks/Data_Engineering_Journey/assets/51254935/bb3e0d7c-a3f2-407d-84b8-b23dd89e151b)

This project helped me to explore and work through different stages of data engineering task. I utilized and integrated the following technologies on this end-to-end project:
- Python – Was the main programming language used for this task.
- Pandas – A python library was used for data manipulation and transformation.
- MySQL connector – A python library for connecting, creating and managing database.
- AWS S3 Services – AWS S3 was used as the Data Lake to store data in its raw data.
- AWS RDS Service – For creating and storing structured data in MySQL object.
- AWS IAm – For creating and managing user access and privileges.
- Tableau – A business intelligence (BI) tool for building dashboard and reports.

#### Project Step and Highlights:
📊 Data Acquisition:  
- The dataset used was Washington DC Service calls Data acquired from the DC's 311 service request center. They represent all service requests such as abandoned automobiles, parking meter repair and bulk trash pickup. The dataset includes Service code, order date, priority, status etc. 

🔵 Data Extraction: 
- The dataset was downloaded using the opendatasets in a geojson format and loaded into S3 bucket.

🛠️ Data Cleaning and Transformation: 
- After data extraction the data was cleaned and transformed into the right model. The following steps were taken in this process: Data format revision, address parsing, data validation and data de_duplication. The final transformed data was stored in S3 bucket object.

𝌭 Data Modeling: 
- Dimensional modelling was used in creating Fact and dimension tables. A star schema was used, the schema was designed, then pandas library was used in slicing and dicing the dataframes in the Python environment.

☁️ Cloud Computing: 
- AWS services were used in the creation and management of both S3 buckets and RDS, boto3 library was used to interact with AWS services using python.

📈 Analytical Report: 
- Using tableau desktop to connect and query the database, creating visuals and building dashboards and reports.

**Dataset Used**:
More info on the dataset here:
- Website: [https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2012/explore?location=39.996028%2C-78.566946%2C8.98&showTable=true](https://opendata.dc.gov/datasets/DCGIS::all-311-city-service-requests-last-30-days/explore?showTable=true)
- Code: https://github.com/Sylvesterchuks/Data_Engineering_Journey/tree/main/Day_30
**My Dashboard**:

![final analysis image](https://github.com/Sylvesterchuks/Data_Engineering_Journey/assets/51254935/35e2e630-12ee-494d-8bd8-9d3f067a33fe)

#100DaysOfDataEngineering #DataEngineering #AnalyticsEngineering #Data #LyftDataAnalysis #AWS #CloudComputing #Python #Tableau #BigDataAnalysis

