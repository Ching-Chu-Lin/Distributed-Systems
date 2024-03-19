package org.apache.hadoop.mapred.lib;

import java.util.HashMap;
import java.util.Random;

import org.apache.hadoop.mapred.lib.HashPartitioner;

public class RandomPartitioner<K, V> extends HashPartitioner<K, V> {
    private Random rand = new Random();
    private HashMap<K, Integer> app_version_random = new HashMap<K, Integer>();

    public int getPartition(K key, V value, int numReduceTasks) {
        Integer sequence = app_version_random.getOrDefault(key, rand.nextInt()); 
        app_version_random.put(key, sequence);
        return (sequence & Integer.MAX_VALUE) % numReduceTasks;
    }
}
