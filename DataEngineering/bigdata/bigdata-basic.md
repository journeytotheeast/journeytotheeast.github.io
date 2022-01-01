# Big data basic

## 2 cents
- The volume of big data is not just more: it's different
- Technology that handles modest volumes of data breaks down with larger volumes of data.

## Volume

### Distributed Storage
- At big data scale, there must be a way to store data in your database - even a single database table across multiple disks.
- A conventional file systems that stores each file on a single disk is not adequate.
- Distribution of data across a large number of disks is the norm with big data.

### Distributed Processing
- Along with distributed storage, processing is typically distributed, which allows parallel processing that speeds up the tasks significantly.
- Complex tasks may require multiple processing stages, including shuffling data among computers. For example, sorting and ordering data cannot be done solely with parallel processing - the data stored in different machines will need to be compared, so shuffling among the machines will be needed.

## Variety
- Structured data
- Unstructured data
- Semi-Structured data: JSON, XML, CSV, logfile

## Velocity
The speed at which data is generated.
### Ingest
Big data systems provide choices for data stores that can hold great volumes and types of data, but there remains the challenges of transferring records from where they originate into your big data store - that is, the ingest of this data. Aside from challenges presented by volume and variety, the velocity of big data production presses the limits of data transmission rates.

As with data processing of high volume of data, systems that address high velocity ingest do so by means of multiple parallel processes. For example, using open source software like [Apache Kafka](http://kafka.apache.org/) and [Apache Flume](http://flume.apache.org/), enterprise can build ingest pipelines composed of hundreds of data stream, transferring petabytes of data daily. These systems use multiple servers and processes to achieve high rates of data throughput between multiple points, using many concurrent transfer paths. [StreamSets](https://streamsets.com/) is open source software that lets designers create, monitor, and maintain data-transfer pipelines using a GUI.

Once data records have been ingested into your big data store, you can contribute to the velocity of gaining insights by learning to write correct queries quickly, using tools such as Apache Impala that can deliver results with low response times. Data analysts, while not mainly concerned with the mechanics of moving data from one data store to another, certainly do care about the timeliness of analytics results. 

### Stream Analytics
Hive and Impala are designed to run against a data set that remains unchanged for the duration of your queries. You need a distinctively different form of processing if you wish to process data records as they are produced.

Such a form is stream analytics, in which analysis is done on data streams while the records are in motion, and prior to the time records come to rest in storage. This involves processing data in one of two ways. One technique is to respond to each record as a data event that can be examined, and which can then trigger some other action like an update on a graphic display or change in a machine setting. The other technique is to use micro-batches, in which the records accumulated over a small time interval, say each second, are gathered and processed quickly to produce a near real-time information point or action in response.

Apache Spark has a subproject focused on stream processing, call [Spark Streaming](http://spark.apache.org/streaming/) and [Apache Storm](http://storm.apache.org/) is an other open source project devoted to stream processing. Proprietary software such as [Splunk](https://www.splunk.com/) focuses on both data transfer and streaming processing. Interestingly, Splunk pipelines can process data records in motion, and bring data to rest by storing it in a Hadoop cluster. This use of different software tools in combination is common in enterprises today.

Spark Streaming, Apache Storm and Splunk each have their own specific programming interfaces for you to do stream analytics. 

## Big Data Systems: How do they differ from traditional systems?

### Strength of RDBMS
1. Enforcing business rules
2. Transactions, OLTP
3. Structure
4. Many good choices
5. Strong with small or medium data
6. Simple security controls
7. Fast (at reasonable scale)

### Limitations of RDBMS
1. Schema on write: Although schema-on-write systems are good when you only want to retain properly structured data, they are poor choices for retaining semi-structured or semi-structured data.
2. High cost of storage
3. Weak support for unstructured data: a large amount of unstructured data would need to be stored as a BLOB or CLOB, RDBMSs provide little or no support for working with such data
4. Difficulty of distributed transactions

## How Structure Affects What You Can Do

### SQL and unstructured data
- User Defined Function (UDF): A function written in a general programming language (such as C, Java, Python) added to the database software by the program user.


## Big Databases, Big Data Storages, and SQL
### Big Data Analytic Databases (Data Warehouse)
- Good for deep analysis; let you ask a lot of questions
- Such as: Apache Impala, Hive, Drill, Presto / Oracle, Teradata (higher cost)

### NoSQL: Operational, Unstructured and Semi-structured
- Good for carefully focused operational applications
- Such as: key-value store like Apache Hbase, cassandra, or document stores like MongoDB and CouchBase

## Features of SQL for Big Data Analysis

### Challenges
- Distributed transactions: Transactions are difficult to scale across large data. The necessity of distributed data storage for big data makes it difficult to ensure multi-statement transactions are ACID. Irregularities in data transfer times can cause conflicts among transactions.
- Data variety: The inability to store data without verifying it first poses difficulties for the large variety of data expected with big data. Big data is messy, unstructured or with issues that would prevent storage by an RDBMS, so the schema-on-write method of RDBMS severely limit the effectiveness of using an RDBMS for big data.

### What We Keep
- SELECT statements, including multi-table SELECTs
- Seeing data as tables with column names
- DDL
- DCL

### What We Give Up
The implications of dropping transactions for big data analytics are:

- Unique values within columns:  loss of checking existing data before adding the new data, so uniqueness within a column cannot be guaranteed.

- Synchronized indexes: loss of maintaining synchronized indexes for changes made on a table.

- Triggers and stored procedures: loss of triggers (which depend on transactions) and stored procedures (which mostly, though not always, require transactions).

### What We Add
- Table partitions and bucketing
- Support for many files format (i.e: binary format for storing structured dataL 
Apache avro, parquet)
- Complex data types

## Different Data Store
### Where To Store Big Data

### Coupling of Data and Metadata
#### CREATING TABLE in a transactional RDBMS
- Check for key consistency
- Set up files
- Set up indexes
- Record table details
 #### A RDBMS's dictionary is tightly coupled with the tables
 The contents of the data dictionary accurately describe every table in the database. 

 #### A big data system's table definition are loosely coupled to files
 The table definitions provide a structure, but there is no guarantee that any of the files will follow that structure. In addition, some files may not be associated with any tables at all.

 - The data dictionary is used to verify data when it's stored (schema on write), while the table definition in a big data system don't touch data when it's being stored - only when it's being loaded in for a query (schema on read). 

## Apache Hive
- Hive translate SQL statements into other programs for actual execution. (MapReduce or Spark)

- Hive is a good choice for processing large amounts of data as part of an ETL pipeline. It's especially good for complicated processing that should be stored back into the cluster.
## Apache Impala
- Is built from the ground up as a SQL engine for big data.
- Is a good choice for quick queries, looking for specific answers.
