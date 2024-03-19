# Env Setup
```bash
$ $HADOOP_HOME/bin/hadoop namenode -format
$ $HADOOP_HOME/sbin/start-dfs.sh
$ $HADOOP_HOME/bin/hadoop fs -put localFile.txt /hdfsFile.txt
```

### Insert Customize Partitioner to MapReduce Streaming
1. Note that Customized Partitioner must under `org.apache.hadoop.mapred.lib` package
2. Compile to `.class` file and make to `jar` file.
```bash
$ $HADOOP_HOME/bin/hadoop com.sun.tools.javac.Main <path to partitioner>
$ jar cf <partitioner jar> <partitioner class> 
```
3. Put jar file under the class path OR Set class path
```bash
$ export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:<…>
$ source .profile 
$ $HADOOP_HOME/bin/hadoop classpath
```

# Run MapReduce
```bash
$ $HADOOP_HOME/bin/bin/mapred streaming -D mapreduce.job.reduces=5 -file <mapper executable/ script> -mapper <mapper executable/ script> -file <reducer executable/ script> -reducer <reducer executable/ script> -input <input file> -output <output dir> -partitioner org.apache.hadoop.mapred.lib.RandomPartitioner
```


# Notes
run job history server but failed:
```bash
$ $HADOOP_HOME/bin/mapred historyserver
```

or 

```bash
$ $HADOOP_HOME/sbin/start-all.sh
```

ports:
1. jobhistory server: 19888
2. resource manager: 8088

### Reference Tried
- [x] https://www.youtube.com/watch?v=Z_5pJMCoeM8
- [x] https://www.youtube.com/watch?v=JgYh5SuV37M
- [x] https://stackoverflow.com/questions/42884289/job-history-server-in-hadoop-2-7-1-is-not-working
    outcome: no running or completed jobs
- [x] https://stackoverflow.com/questions/22921102/how-to-find-total-number-of-nodes-on-which-hadoop-is-installed 
    outcome: exception error
