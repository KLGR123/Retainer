using UnityEngine;

public class CharacterControl : MonoBehaviour
{
    // Speed at which the character moves left and right
    public float moveSpeed = 5f;

    // Reference to the Rigidbody component
    private Rigidbody rb;

    // Start is called before the first frame update
    void Start()
    {
        // Get the Rigidbody component attached to the character
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        // Get horizontal input (A/D keys or Left/Right arrows)
        float horizontalInput = Input.GetAxis("Horizontal");

        // Calculate the new position based on input and speed
        Vector3 newPosition = transform.position + Vector3.right * horizontalInput * moveSpeed * Time.deltaTime;

        // Update the character's position
        rb.MovePosition(newPosition);
    }

    // This method will be called when the character collides with another object
    private void OnCollisionEnter(Collision collision)
    {
        // Check if the character collided with an obstacle
        if (collision.gameObject.CompareTag("Obstacle"))
        {
            // End the game if the character hits an obstacle
            GameOver();
        }

        // Check if the character collided with a collectible item
        if (collision.gameObject.CompareTag("Collectible"))
        {
            // Increase the score
            CollectItem(collision.gameObject);
        }
    }

    // Method to handle game over logic
    private void GameOver()
    {
        // Implement game over logic here
        Debug.Log("Game Over!");
        // For example, stop the game or show a game over screen
    }

    // Method to handle item collection
    private void CollectItem(GameObject collectible)
    {
        // Implement item collection logic here
        Debug.Log("Item Collected!");
        // For example, increase score and destroy the collectible
        Destroy(collectible);
    }
}