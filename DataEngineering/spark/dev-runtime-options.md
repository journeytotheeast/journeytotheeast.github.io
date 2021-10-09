# Development and runtime options

- Spark Architecture has driver and executor processes, coordinated by the Spark Context in the Driver.

- The Driver creates jobs and the Spark Context splits jobs into tasks which can be run in parallel in the executors on the cluster.

- Stages is a set of tasks that are separated by a data shuffle. Shuffles are costly, as they require data serialization, disk and network I/O. The driver program can be run in either client mode (connecting the driver outside the cluster) or cluster mode (running the driver in the cluster).

- Cluster managers acquire resources and run as an abstracted service outside the application. Spark can run on Spark Standalone, Apache Spark YARN, Apache Mesos or Kubernetes cluster managers, with specific set-up requirements. Choosing a cluster manager depends on your data ecosystem and factors as ease of configuration, portability, deployment, or data partitioning needs. Spark can also run using loal mode, which is useful for testing, debugging an application.

- `spark-submit` is a unified interface to submit the Spark application, no matter the cluster manager or application language. Mandatory options include telling Spark which cluster manager to connect to; other options set driver deploy mode or executor resourcing. To manage dependencies, application projects or libraries must be accessible for the driver and executor processes, for example by creating a Java or Scala uber-JAR. Spark Shell simplifies working with data by automatically initializing the SparkContext and SparkSession variable and providing Spark API access.