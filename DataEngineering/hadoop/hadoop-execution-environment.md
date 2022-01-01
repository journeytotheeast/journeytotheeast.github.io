# The Hadoop Execution Environment

### Recall Hadoop Architecture
- Data distributed across nodes
- Keep compute task on the node with data

### MapReduce Execution Framework
- Software framework
- Schedules, monitors, and manages tasks
- Works for Applications that fits MapReduce Paradigm
- What if: Iterative data exploration/ Iterative data processing???
  -> NextGen Execution Frameworks: support complex DAG of tasks and in-memory caching of data


## Execution frameworks: YARN, Tez, Spark
### YARN
- Support MapReduce
- User developed applications: You can write your own user developed application that run through YARN. You will have to write the application master and all the managing of tasks.
- Frameworks like Tez, Spark that sit on top of YARN. They talk to YARN for the resource requirements, but other than that they have their own mechanisms and self-supporting applications.

### Tez
- Dataflow graphs
- Custom data types: No restriction like a key value pair on MapReduce framework
- Can run complex DAG of tasks
- Dynamic DAG changes
- Resource usage efficiency

- Hive on Tez example:
```sql
SELECT a.vendor, COUNT(*), AVG(c.cost)
FROM 
  a
  JOIN
  b
  ON (a.id = b.id)
  JOIN
  c
  ON (a.itemid = c.itemid)
GROUP BY a.vendor 
```

### Spark
- Advanced DAG execution engine
- 

## Hadoop Resource Scheduling
- Resource management
- Different kind of scheduling algorithms
- Type of parameters that can be controlled

### Motivations for Schedulers
- Various execution engines
- Schedule / Performance: if you just let Hadoop schedule by their default mechanism, you could end up with issues with scheduling like an important job that needs dedicated resources, might end up waiting a long time.
- Control of resources between components

### Schedulers
- Default (FIFO)
- Fairshare: balance out the resources across applications over time
- Capacity: you can have a guaranteed capacity for each application or group, and there are safeguards to prevent a user or an application from taking down the whole cluster by running it out of resources.

## Hadoop-Based Application
- Overview of apps, high level languages, services

### Databases/Stores
- Avro: data structures within the context of Hadoop MapReduce jobs
- Hbase: distributed non-relational database
- Cassandra: distributed data management system

### Querying
- **Pig**: Platform for analyzing large data sets in HDFS
- **Hive**: Query and manage large datasets
- **Impala**: High-performance, low-latency SQL querying of data in Hadoop file formats
- **Spark**: General processing engine for streaming, SQL, ...

### Apache Pig
- Platform for data processing
- Pig Latin: High level language, can do the scripting
- Pig execution environment: Local, MapReduce, Tez
- In built operators and functions: math functions, ...
- Extensible
- Usage areas:
  - Extract, Transform, Load (ETL) operations
  - Manipulating, analyzing `raw` data
- Example:
```sh
dhfs dfs -put /etc/passwd /user/cloudera
pig mapreduce
```


### Apache Hive
- Data warehouse software
- HiveQL: SQL like language to structure and query data
- Execution environment: MapReduce, Tez, Spark
- Data in HDFS, Hbase
- Custom mappers/reducers
- Usage areas: Data mining, analytics, machine learning, Adhoc analysis
- Example:
  - start by loading the file into HDFS: 
  ```sh
  hdfs dfs -put /etc/passwd /tmp  
  ```
  - run beeline to access interactively
  ```sh
  beeline -u jdbc:hive2://
  ```

### Apache HBase
- Scalable data store
- Non-relational distributed database
- Run on top of HDFS
- Compression: 
- In-memory operations: MemStore, BlockCache
- HBase Features:
  - Consistency: if you transition a table from a valid state to another, it basically happens directly without intermediate changes.
  - High Availability
  - Automatic Sharding
  - Replication
  - SQL like access: Hive, Impala
- Example:
```sh
hbase shell
```
