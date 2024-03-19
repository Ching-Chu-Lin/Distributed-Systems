package org.apache.hadoop.mapred.lib;

import java.util.HashMap;

import org.apache.hadoop.mapred.lib.HashPartitioner;


public class RoundRobinPartitioner<K, V> extends HashPartitioner<K, V> {
    private HashMap<K, Integer> app_version_counter = new HashMap<K, Integer>();

    public int getPartition(K key, V value, int numReduceTasks) {
        Integer sequence = app_version_counter.getOrDefault(key, app_version_counter.size()); 
        app_version_counter.put(key, sequence);
        return (sequence & Integer.MAX_VALUE) % numReduceTasks;
    }

}
