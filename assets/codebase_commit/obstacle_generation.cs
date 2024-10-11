using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObstacleGeneration : MonoBehaviour
{
    public GameObject obstaclePrefab; // The prefab for the obstacles
    public float spawnInterval = 2.0f; // Time interval between spawns
    public float riverWidth = 10.0f; // Width of the river
    public float obstacleSpeed = 5.0f; // Speed at which obstacles move down the river

    private float timer = 0.0f; // Timer to track spawn intervals

    void Start()
    {
        // Initialize the timer
        timer = spawnInterval;
    }

    void Update()
    {
        // Update the timer
        timer -= Time.deltaTime;

        // Check if it's time to spawn a new obstacle
        if (timer <= 0.0f)
        {
            SpawnObstacle();
            timer = spawnInterval; // Reset the timer
        }
    }

    void SpawnObstacle()
    {
        // Randomly determine the x position within the river width
        float xPosition = Random.Range(-riverWidth / 2, riverWidth / 2);

        // Create a new obstacle at the determined position
        Vector3 spawnPosition = new Vector3(xPosition, transform.position.y, transform.position.z);
        GameObject newObstacle = Instantiate(obstaclePrefab, spawnPosition, Quaternion.identity);

        // Set the obstacle's speed
        Rigidbody obstacleRigidbody = newObstacle.GetComponent<Rigidbody>();
        if (obstacleRigidbody != null)
        {
            obstacleRigidbody.velocity = new Vector3(0, 0, -obstacleSpeed);
        }
    }
}