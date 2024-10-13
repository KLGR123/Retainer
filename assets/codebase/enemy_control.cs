using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyControl : MonoBehaviour
{
    public float speed = 1.0f; // The speed at which the enemy moves
    public int health = 100; // The health of the enemy
    public int damage = 10; // The damage the enemy does to the carrot
    public Transform[] waypoints; // The waypoints the enemy will follow
    private int currentWaypointIndex = 0; // The current waypoint index the enemy is moving towards

    // Start is called before the first frame update
    void Start()
    {
        // Initialize the enemy's position to the first waypoint
        transform.position = waypoints[currentWaypointIndex].position;
    }

    // Update is called once per frame
    void Update()
    {
        MoveAlongPath();
    }

    // Method to move the enemy along the path defined by waypoints
    void MoveAlongPath()
    {
        if (currentWaypointIndex < waypoints.Length)
        {
            // Move towards the next waypoint
            transform.position = Vector3.MoveTowards(transform.position, waypoints[currentWaypointIndex].position, speed * Time.deltaTime);

            // Check if the enemy has reached the waypoint
            if (Vector3.Distance(transform.position, waypoints[currentWaypointIndex].position) < 0.1f)
            {
                currentWaypointIndex++;
            }
        }
        else
        {
            // If the enemy reaches the end of the path, it should damage the carrot
            ReachCarrot();
        }
    }

    // Method to handle the enemy reaching the carrot
    void ReachCarrot()
    {
        // Implement logic to damage the carrot
        Debug.Log("Enemy reached the carrot and dealt " + damage + " damage.");
        Destroy(gameObject); // Destroy the enemy after reaching the carrot
    }

    // Method to apply damage to the enemy
    public void TakeDamage(int amount)
    {
        health -= amount;
        if (health <= 0)
        {
            Die();
        }
    }

    // Method to handle the enemy's death
    void Die()
    {
        // Implement logic for enemy death, such as playing a death animation or dropping loot
        Debug.Log("Enemy died.");
        Destroy(gameObject);
    }
}