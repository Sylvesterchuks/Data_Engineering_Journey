## Day 2: Dynamic and Evolution of Data Engineering Work in an Organization. 👇
The purpose of Data engineering is to take data and make it available for analysis. A click on the YouTube video, click the like button 👍of a video or comment ✍🏻on a video and data is saved to the database for analysis. Today I learnt about the work of data engineering and how these processes change over time.

An analytics team wants to reduce the manual workload and automate the data movement from source to destination. This is where data engineering comes in, starts with automation using a simple ETL(Extract-Transform-Load) pipeline; the goal is to automatically pull data from all sources and load them unto a database, allowing the analytics team to focus more on the analysis, dashboarding etc.

Because the above pipeline uses a standard transactional database, as the data increases, queries take longer time to execute; the current pipeline doesn’t seem like a viable option anymore.😔

A new concept is introduced data warehouse. Data warehouse is a repository that consolidates data in a single central place. Data warehouse is completely optimized to run complex queries unlike the standard transactional databases. Problem solved, queries are executed faster and all seems well, but it doesn’t stop there👻.

The data warehouse being structured to report metrics that are already defined in advance, might not provide enough data for task like discovering patterns, building predictive models etc. While maintaining the existing pipeline, the data engineering team creates a custom ETL pipeline to serve this specific purpose. Additionally, a data lake (Data Lake is a type of storage that keeps all the data without preprocessing it and imposing a defined schema) is designed using ELT (Extract-Load-Transform) pipeline for the purpose of building predictive models. In the above data pipeline scenarios, all the data were processed in batches, scheduled to run at interval e.g., every month, week or hour.

Data lake is an artifact for big data. Think of streaming services like YouTube that collects millions of services every second. Big data is characterized by 4Vs (Volume, Variety, Veracity, Velocity). Unlike other pipelines, big data pipeline runs data every second (in Real time). For Big data pipeline, data is streamed and processed using a Pub/Sub systems like Kafka and big data processing ETL/ELT e.g., Apache Spark and then loaded into data lakes, data warehouses or custom ETL, these data repositories are deployed on clusters of several servers that run with tools for distributed storage like Hadoop, and can be consumed by every stakeholder for further analysis.

This is how a data engineering work evolved from a simple database ETL pipeline to a complex big data pipeline.

Thanks 🙏🏼 to [AltexSoft](https://www.linkedin.com/company/altexsoft/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_recent_activity_content_view%3BPuoWYJ2hQWeTyCUgyB3pcA%3D%3D), this summary was written after watching their video “How Data Engineering Works”.
Video link in the comments.
#100DaysOfDataEngineering #DataEngineering
