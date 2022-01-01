# Hadoop Application Framework

- HBase - a scalable data warehouse with support for large tables.
- Hive - a data warehouse infrastructure that provides data summarization and ad hoc querying
- Pig - a high-level data-flow language and execution framework for parallel computation.
- Spark - a fast and general compute engine for Hadoop data. Wide range of applications - ETL, Machine Learning, stream processing, and graph analytics.

## HDFS2
### HDFS Design Concept
- Using a lot of nodes
- Scalable distributed filesystem
- Distributed data on local disks on several nodes
- Low cost commodity hardware

### Original HDFS Design Goals
- Resilience
- Scalable
- Application Locality
- Portability

### Original HDFS Design
- Single NameNode
- Multiple DataNodes
  - Manage storage - blocks of data
  - Serving read/write requests from clients
  - Block creation, deletion, replication

### HDFS in Hadoop2
- **HDFS Federation**
    - Benefits:
      - Increased namespace scalability
      - Performance
      - Isolation

- How its done
  - Multiple Namenode servers
  - Multiple namespaces
  - Block pools

- High Availability - redundant NameNodes
- Heterogeneous Storage and Archival Storage
  - ARCHIVE, DISK, SSD, RAM_DISK

### MapReduce Framework & YARN

#### MapReduce framework
- Software framework - for writing parallel data processing applications
- MapReduce job splits data into chunks
- Map tasks process data chunks
- Framework sorts map output
- Reduce tasks use sorted map data as input
- Typically compute and storage nodes are the same.
- MapReduce tasks and HDFS running on the same nodes.
- Can schedule tasks on nodes with data already present.

#### Original MapReduce Framework
- Single master JobTracker
- JobTracker schedules, monitors, and re-executes failed tasks.
- One slave TaskTracker per cluster node.
- TaskTracker executes tasks per JobTracker requests.

#### YARN: NexGen MapReduce
- Main idea: Separate resource management and job scheduling/monitoring.
- Global ResourceManager
- NodeManager on each node
- Application Master - one for each application

#### Additional YARN Features
- High Availability ResourceManager
- Timeline Server
- Use of Cgroups: which is a Linux feature, to manage resources used by the containers.
- Secured Containers
- YARN - web services REST APIs


