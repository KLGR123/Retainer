using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PipeControl : MonoBehaviour
{
    public float speed = 2.0f; // Speed at which the pipes move towards the bird
    public float resetPositionX = -10.0f; // X position at which pipes will reset to the start
    public float startPositionX = 10.0f; // X position where pipes start moving from
    public float minY = -1.0f; // Minimum Y position for the gap between pipes
    public float maxY = 3.0f; // Maximum Y position for the gap between pipes

    private Vector2 startPosition;

    void Start()
    {
        // Initialize the start position of the pipes
        startPosition = new Vector2(startPositionX, Random.Range(minY, maxY));
        transform.position = startPosition;
    }

    void Update()
    {
        // Move the pipes to the left at a constant speed
        transform.Translate(Vector2.left * speed * Time.deltaTime);

        // Check if the pipes have moved past the reset position
        if (transform.position.x < resetPositionX)
        {
            // Reset the pipes to the start position with a new random Y position
            ResetPipes();
        }
    }

    void ResetPipes()
    {
        // Set a new random Y position for the gap between the pipes
        float newY = Random.Range(minY, maxY);
        transform.position = new Vector2(startPositionX, newY);
    }
}