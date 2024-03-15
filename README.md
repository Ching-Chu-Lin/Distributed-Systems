env setup:
```bash
$ $HADOOP_HOME/bin/hadoop namenode -format
$ $HADOOP_HOME/sbin/start-dfs.sh
```

run job history server (but failed):
```bash
$ $HADOOP_HOME/bin/mapred historyserver
```
open master-ip:19888

run map reduce:
```bash
$ $HADOOP_HOME/bin//mapred streaming -D mapreduce.job.reduces=5 -file ~/mapper.py -mapper ~/mapper.py -file ~/reducer.py -reducer ~/reducer.py -input /big_movies.csv -output /key_5 -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
```
