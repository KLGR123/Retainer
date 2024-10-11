using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ItemGeneration : MonoBehaviour
{
    public GameObject[] items; // Array to hold different item prefabs
    public float spawnInterval = 2.0f; // Time interval between item spawns
    public float riverWidth = 10.0f; // Width of the river for item spawning
    private float nextSpawnTime = 0.0f; // Time when the next item should spawn

    void Start()
    {
        // Initialize the next spawn time
        nextSpawnTime = Time.time + spawnInterval;
    }

    void Update()
    {
        // Check if it's time to spawn a new item
        if (Time.time >= nextSpawnTime)
        {
            SpawnItem();
            // Update the next spawn time
            nextSpawnTime = Time.time + spawnInterval;
        }
    }

    void SpawnItem()
    {
        // Randomly select an item from the array
        int itemIndex = Random.Range(0, items.Length);
        GameObject itemToSpawn = items[itemIndex];

        // Randomly determine the spawn position within the river width
        float spawnXPosition = Random.Range(-riverWidth / 2, riverWidth / 2);
        Vector3 spawnPosition = new Vector3(spawnXPosition, transform.position.y, transform.position.z);

        // Instantiate the item at the calculated position
        Instantiate(itemToSpawn, spawnPosition, Quaternion.identity);
    }
}