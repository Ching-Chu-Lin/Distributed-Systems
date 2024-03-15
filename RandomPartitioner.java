import java.util.HashMap;
import java.util.Random;

import org.apache.hadoop.mapreduce.Partitioner;

public class RandomPartitioner<K, V> extends Partitioner<K, V> {
    private Random rand = new Random();
    private HashMap<K, Integer> app_version_random = new HashMap<K, Integer>();

    public int getPartition(K key, V value, int numReduceTasks) {
        Integer sequence = app_version_random.getOrDefault(key, rand.nextInt()); 
        return (sequence & Integer.MAX_VALUE) % numReduceTasks;
    }
}
