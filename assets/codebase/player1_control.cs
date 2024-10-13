using UnityEngine;

public class Player1Control : MonoBehaviour
{
    // Public variables for player settings
    public float swingSpeed = 2.0f; // Speed of the swinging motion
    public float throwSpeed = 5.0f; // Speed at which the claw is thrown
    public float retractSpeed = 3.0f; // Speed at which the claw retracts

    // Private variables for internal state
    private bool isSwinging = true; // Is the claw currently swinging?
    private bool isThrown = false; // Is the claw currently thrown?
    private Vector3 targetPosition; // The target position for the claw when thrown
    private GameObject grabbedObject = null; // The object currently grabbed by the claw

    // Update is called once per frame
    void Update()
    {
        if (isSwinging)
        {
            HandleSwinging();
        }
        else if (isThrown)
        {
            HandleThrowing();
        }
        else if (grabbedObject != null)
        {
            HandleRetracting();
        }

        // Check for player input to throw the claw
        if (Input.GetMouseButtonDown(0) && isSwinging)
        {
            ThrowClaw();
        }
    }

    // Handle the swinging motion of the claw
    private void HandleSwinging()
    {
        // Implement swinging logic here
        // For example, rotate the claw back and forth
        transform.Rotate(Vector3.forward, Mathf.Sin(Time.time * swingSpeed) * swingSpeed);
    }

    // Handle the throwing motion of the claw
    private void HandleThrowing()
    {
        // Move the claw towards the target position
        transform.position = Vector3.MoveTowards(transform.position, targetPosition, throwSpeed * Time.deltaTime);

        // Check if the claw has reached the target position
        if (transform.position == targetPosition)
        {
            // Check for collision with objects
            CheckForObjectCollision();
        }
    }

    // Handle the retracting motion of the claw
    private void HandleRetracting()
    {
        // Move the claw back to the starting position
        transform.position = Vector3.MoveTowards(transform.position, Vector3.zero, retractSpeed * Time.deltaTime);

        // Check if the claw has returned to the starting position
        if (transform.position == Vector3.zero)
        {
            // Release the grabbed object
            ReleaseObject();
        }
    }

    // Throw the claw towards a target
    private void ThrowClaw()
    {
        isSwinging = false;
        isThrown = true;
        // Calculate the target position based on the current direction
        targetPosition = transform.position + transform.up * 10.0f; // Example distance
    }

    // Check for collision with objects
    private void CheckForObjectCollision()
    {
        // Implement collision detection logic here
        // For example, use a raycast or collision detection to find objects
        // If an object is hit, grab it
        RaycastHit hit;
        if (Physics.Raycast(transform.position, transform.up, out hit, 1.0f))
        {
            if (hit.collider.CompareTag("Gold") || hit.collider.CompareTag("Stone") || hit.collider.CompareTag("Diamond"))
            {
                grabbedObject = hit.collider.gameObject;
                isThrown = false;
            }
        }
    }

    // Release the grabbed object
    private void ReleaseObject()
    {
        // Implement logic to handle the grabbed object
        // For example, calculate score based on object type
        if (grabbedObject != null)
        {
            if (grabbedObject.CompareTag("Gold"))
            {
                // Add normal score
            }
            else if (grabbedObject.CompareTag("Stone"))
            {
                // Add low score
            }
            else if (grabbedObject.CompareTag("Diamond"))
            {
                // Add high score
            }

            // Destroy or deactivate the object
            Destroy(grabbedObject);
            grabbedObject = null;
        }

        // Reset to swinging state
        isSwinging = true;
    }
}