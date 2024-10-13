using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PipeControl : MonoBehaviour
{
    public float speed = 2.0f; // Normal movement speed of the pipes
    public float suddenMoveDistance = 2.0f; // Distance for sudden movement
    public float suddenMoveInterval = 3.0f; // Time interval for sudden movement
    private float nextSuddenMoveTime = 0.0f; // Time when the next sudden move should occur

    private Vector3 startPosition;

    void Start()
    {
        // Store the initial position of the pipes
        startPosition = transform.position;
        // Schedule the first sudden move
        nextSuddenMoveTime = Time.time + suddenMoveInterval;
    }

    void Update()
    {
        // Move the pipes to the left at a constant speed
        transform.Translate(Vector3.left * speed * Time.deltaTime);

        // Check if it's time for a sudden move
        if (Time.time >= nextSuddenMoveTime)
        {
            SuddenMove();
            // Schedule the next sudden move
            nextSuddenMoveTime = Time.time + suddenMoveInterval;
        }

        // Reset the position of the pipes if they move out of the screen
        if (transform.position.x < -10)
        {
            ResetPosition();
        }
    }

    void SuddenMove()
    {
        // Randomly decide to move the pipe up or down
        float moveDirection = Random.Range(0, 2) == 0 ? -1 : 1;
        // Calculate the new position with sudden movement
        Vector3 suddenMove = new Vector3(0, moveDirection * suddenMoveDistance, 0);
        transform.position += suddenMove;
    }

    void ResetPosition()
    {
        // Reset the position of the pipes to the start position
        transform.position = startPosition;
    }
}