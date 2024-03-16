env setup:
```bash
$ $HADOOP_HOME/bin/hadoop namenode -format
$ $HADOOP_HOME/sbin/start-dfs.sh
$ $HADOOP_HOME/bin/hadoop fs -put localFile.txt /hdfsFile.txt
```
open master-ip:9870

run job history server (but failed):
```bash
$ $HADOOP_HOME/bin/mapred historyserver
```

or 

```bash
$ $HADOOP_HOME/sbin/start-all.sh
```

open master-ip:19888

tried references:
1. https://docs.cloudera.com/HDPDocuments/HDP2/HDP-2.0.0.2/bk_installing_manually_book/content/rpm-chap4-4.html
2. 

run map reduce:
```bash
$ $HADOOP_HOME/bin/mapred streaming -D mapreduce.job.reduces=5 -file ~/mapper.py -mapper ~/mapper.py -file ~/reducer.py -reducer ~/reducer.py -input <input file> -output <output dir> -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
```
