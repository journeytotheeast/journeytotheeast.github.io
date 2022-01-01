# Introduction to HDFS

## Overview of HDFS
### HDFS Design Concept
- Scalable distributed filesystem
- Distributed data on local disks on several nodes
- Low cost commodity hardware

### HDFS Design Factors
- Hundreds/Thousands of nodes => Need to handle node/disk failures
- Portability across heterogeneous hardware/software
- Handle large data sets
- High throughput

### Approach to meet HDFS design goals
- Simplified coherency model - write once read many
- Data Replication - helps handle hardware failures
- Move computation close to data
- Relax POSIX requirements - increase throughput

### Summary of HDFS Architecture
- Single NameNode - a master server that manages the file system namespace and regulates access to files by clients
- Multiple DataNode - typically one per node in the cluster. Functions:
  - Manage storage
  - Serving read/write requests from clients
  - Block creation, deletion, replication based on instruction from the NameNode

## The HDFS Performance Envelope
- Able to determine number of blocks for a given file size
- Key HDFS and system components impacted by block size
- Impact of small files on HDFS and system

### HDFS block size
- Default block size is 64MB
- Good for large files
- So a 10GiB file will be broken into: 10*1024/64 = 160 blocks.

### Importance of #blocks in a file
- NameNode memory usage: Every block represented as object, each object uses a bit of the memory in the NameNode (default replication this will be further increase 3X)
- Number of map tasks: data typically processed block at a time

### Large #small files: Impact on NameNode
- Memory usage: 
  - for example: ~150 bytes per object
  - 1 billion objects => 300GB memory!
- Network load - Number of checks with datanodes proportional to number of blocks.

### Large #small files: Performance Impact
- Map Task - depends on #blocks
10GB of data, 32K file size => 327680 map tasks
=> lots of queued tasks (typically a cluster may have 100 nodes, and maybe 4 or 8 slots per node)
=> large overhead of spin up/tear down for each task
=> Inefficient disk I/O with small size

### HDFS optimized for large files
- Key takeaway - lots of small files is bad
- Solutions:
  - Merge/Concatenate files
  - Sequence files
  - HBase, HIVE configuration
  - CombineFileInputFormat

### Read/Write Processes in HDFS
#### Write Process in HDFS
- Client request to create file (the data is cached locally on the client, and as it reaches a particular size, like typically a block size, it's going to contact the NameNode and get more information on where that block should go) -> This initial caching is client side buffering, and give you better write throughput, and there's POSIX requirement relaxation.
- NameNode contacted once a block of data is accumulated.
- NameNode responds with a list of DataNodes
- Rack aware
  - for example: the primary replica block is placed on the local Rack (assuming that the HDFS client is in rack 1)
  - the next replica goes on remote rack (rack 2)
  - the 3rd block is on the same remote rack as the 2nd block (rack 2) to minimize network traffic between racks
- The client gets a list of DataNodes back
- First DataNode receives data, write to local and forwards to second DataNode (so the DataNode can be receive data and forward data at the same time in a pipeline -> you're not gonna take 3X the amount of time to make 3 copies of your block)
- NameNode commits file creation into persistent store
  - Once all the blocks are written, and the file flow is done, essentially this process is committed into a persistent state by the NameNode.
  - Receives heartbeat and block reports from all the DataNodes. If there is a failure of the DataNode, the heartbeat is gonna go away, or maybe you get a corrupted block.


#### Read Process in HDFS
- Client gets DataNodes list from NameNode: gets information about the blocks, how they're laid out
- Read from replica closest to reader

## HDFS Performance and Tunning
configuration file: `hdfs-site.xml`
### HDFS Block Size
- Recall: impacts NameNode memory, number of maps tasks, and hence performance
- 64 MB is the default. Can be changed based on workloads. Typically bumped up to 128MB.
- `dfs.blocksize`, `dfs.block.size`

### HDFS Replication
- Default replication is 3
- Parameter: `dfs.replication`
- Tradeoff:
  - Lower it to reduce replication cost
  - Less robust
  - Higher data replication can make data local to more workers
  - Lower replication => more space

### HDFS Performance and Robustness
#### Common Failures:
- DataNode Failures: Server can fail, disk can crash, data corruption
- Network Failures
- NameNode Failures: Disk failure, node failure

#### HDFS Robustness
- NameNode receives heartbeat and block reports from DataNodes

#### Mitigation of common failures
1. Periodic heartbeat: from DataNode to NameNode
- DataNodes with recent heartbeat:
  - Marked dead, no new IO sent: If the periodic heartbeat stops for some reason, the NameNode doesn't receive a recent heartbeat, it will mark the DataNode as dead and any new IO that comes up is not going to be sent to that DataNode.
  - Blocks below replication factor re-replicated on other nodes: The NameNode has information on all the replication information for the files on the file system, so if it knows that a DataNode fails, which blocks fall below that replication factor and the NameNode will restart the process to re-replicate these blocks on other nodes that are still connected.
2. Data corruption:
- Checksum computed on file creation 
- Checksums stored in HDFS namespace
- Used to check retrieved data.
re-read from alternative replication if need
3. Problems with NameNode
- Multiple copies of central meta data structures.
- Failover to Standby NameNode - manual by default

#### Performance
`Changing blocksize and replication factor can improve performance`
- example: Distributed copy
  - Hadoop `distcp` allows parallel transfer of files
  - Copy 32 files and 512GB of data
  - Vary map and node counts, replication

#### Replication trade off w.r.t robustness
- Reducing replication has a trade off w.r.t robustness:
  - Might lose a node or local disk during the run - cannot recover if there is no replication
  - If there is a data corruption of a block from one of the datanodes - cannot recover without replication

## HDFS Access Options, Applications

- HDFS Commands:
invoked via `bin/hdfs` script
- Application Programming Interfaces:
  - Native Java API: Base class org.apache.hadoop.fs.FileSystem
  - C API for HDFS: libhdfs, header file (hdfs.h)
  - WebHDFS REST API: HTTP Get, Put, Post, and Delete operations

- HDFS NFS Gateway

- Apache Flume
- Apache Sqooq

### Applications using HDFS
- Can use APIs to interact with HDFS
- Core component of Hadoop stack - used by all applications
- HBase is a application that runs on top of HDFS with good integration
- Spark can run directly on HDFS without other Hadoop components

### HDFS commands
- List files in /: `hdfs dfs -ls /`
- Make a directory: `hdfs dfs -mkdir /user/test`
- Create a local file & it into HDFS:
  - Create a file with random data using the Unix utility dd (1GB local file called sample.txt on the local filesystem): `dd if=/dev/urandom of=sample.txt bs=64M count=16`
  - `hdfs dfs -put sample.txt /user/test`
  - `hdfs fsck /user/test/sample.txt`
- `hdfs dfsadmin -report`

### Native Java API for HDFS
- Overview:
  - Base class: org.apache.hadoop.fs.FileSystem
  - Important classes:
    - FSDataInputStream
    - FSDataOutputStream
  - Methods: get, open, create

- FSDataInputStream methods:
  - `read`: read bytes
  - `readFully`: read from stream to buffer
  - `seek`: seek to given offset
  - `getPos`: get current position in stream

- FSDataOutputStream methods:
  - `getPos`: get current position in Stream
  - `hflush`: flush out the data in client's user buffer
  - `close`: close the underlying output stream

- Example reading from HDFS using API:
  - get an instance of FileSystem: `FileSystem fs = FileSystem.get(URI.create(uri),conf);`
  - open an input stream
  `in = fs.open(new Path(uri));`
  - Use IO utilities to copy from input stream `IOUtils.copyBytes(in, System.out,4096,false);`
  - Close the stream `IOUtils.closeStream(in);`
- Example writing to HDFS using API:
  - get an instance of the FileSystem `FileSystem fs = FileSystem.get.(URI.create(outuri),conf);`
  - create a file `out = fs.create(new Path(outuri));`
  - write to output stream `out.write(buffer, 0, nbytes);`
  - close the file `out.close()`

### WebHDFS REST API
- Enabling WebHDFS in `/etc/hadoop/conf/hdfs-site.xml`
  - `dfs.webhdfs.enabled`
  - `dfs.web.authentication.kerberos.principal`
  - `dfs.web.authentication.kerberos.keytab`
- Authentication
  - If security is off: 
  - Kerberos

- HTTP GET requests

- HTTP PUT requests: `curl -i -X PUT`

- Example: create a local file and 
