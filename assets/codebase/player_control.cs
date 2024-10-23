using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerControl : MonoBehaviour
{
    public GameObject diggingTool; // The digging tool object
    public float swingSpeed = 2.0f; // Speed of the swinging motion
    public float throwSpeed = 10.0f; // Speed at which the tool is thrown
    public float retractSpeed = 5.0f; // Speed at which the tool retracts
    public int score = 0; // Player's score

    private bool isSwinging = true; // Is the tool currently swinging
    private bool isRetracting = false; // Is the tool currently retracting
    private Vector3 initialPosition; // Initial position of the tool
    private Vector3 targetPosition; // Target position when the tool is thrown
    private GameObject caughtObject; // The object currently caught by the tool

    void Start()
    {
        initialPosition = diggingTool.transform.position;
    }

    void Update()
    {
        if (isSwinging)
        {
            SwingTool();
        }

        if (Input.GetMouseButtonDown(0))
        {
            if (isSwinging)
            {
                ThrowTool();
            }
        }

        if (isRetracting)
        {
            RetractTool();
        }
    }

    // Function to handle the swinging motion of the tool
    void SwingTool()
    {
        float angle = Mathf.PingPong(Time.time * swingSpeed, 90) - 45;
        diggingTool.transform.rotation = Quaternion.Euler(0, 0, angle);
    }

    // Function to throw the tool
    void ThrowTool()
    {
        isSwinging = false;
        targetPosition = diggingTool.transform.position + diggingTool.transform.up * 10.0f;
        StartCoroutine(MoveTool(targetPosition, throwSpeed));
    }

    // Coroutine to move the tool to a target position
    IEnumerator MoveTool(Vector3 target, float speed)
    {
        while (Vector3.Distance(diggingTool.transform.position, target) > 0.1f)
        {
            diggingTool.transform.position = Vector3.MoveTowards(diggingTool.transform.position, target, speed * Time.deltaTime);
            yield return null;
        }

        if (!isRetracting)
        {
            isRetracting = true;
        }
    }

    // Function to retract the tool
    void RetractTool()
    {
        if (caughtObject != null)
        {
            // Move the caught object with the tool
            caughtObject.transform.position = diggingTool.transform.position;
        }

        if (Vector3.Distance(diggingTool.transform.position, initialPosition) > 0.1f)
        {
            diggingTool.transform.position = Vector3.MoveTowards(diggingTool.transform.position, initialPosition, retractSpeed * Time.deltaTime);
        }
        else
        {
            isRetracting = false;
            isSwinging = true;

            if (caughtObject != null)
            {
                // Calculate score based on the type of object caught
                if (caughtObject.CompareTag("Gold"))
                {
                    score += 100; // Normal score for gold
                }
                else if (caughtObject.CompareTag("Rock"))
                {
                    score += 10; // Less score for rock
                }

                Destroy(caughtObject);
                caughtObject = null;
            }
        }
    }

    // Function to handle collision with objects
    void OnTriggerEnter2D(Collider2D other)
    {
        if (!isSwinging && !isRetracting)
        {
            if (other.CompareTag("Gold") || other.CompareTag("Rock"))
            {
                caughtObject = other.gameObject;
                isRetracting = true;

                // Adjust retract speed based on object type
                if (caughtObject.CompareTag("Gold"))
                {
                    retractSpeed = 5.0f; // Normal speed for gold
                }
                else if (caughtObject.CompareTag("Rock"))
                {
                    retractSpeed = 2.5f; // Slower speed for rock
                }
            }
        }
    }
}