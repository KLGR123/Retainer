using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bird : MonoBehaviour
{
    // The force applied to the bird when the player taps the screen
    public float flapForce = 5f;
    // The gravity scale applied to the bird
    public float gravityScale = 1f;
    // Rigidbody2D component of the bird
    private Rigidbody2D rb;

    // Start is called before the first frame update
    void Start()
    {
        // Get the Rigidbody2D component attached to the bird
        rb = GetComponent<Rigidbody2D>();
        // Set the gravity scale of the Rigidbody2D
        rb.gravityScale = gravityScale;
    }

    // Update is called once per frame
    void Update()
    {
        // Check if the player has tapped the screen
        if (Input.GetMouseButtonDown(0))
        {
            // Apply an upward force to the bird
            Flap();
        }
    }

    // Method to apply an upward force to the bird
    void Flap()
    {
        // Reset the bird's vertical velocity
        rb.velocity = new Vector2(rb.velocity.x, 0);
        // Apply a force to the bird's Rigidbody2D to make it "flap"
        rb.AddForce(Vector2.up * flapForce, ForceMode2D.Impulse);
    }

    // Method to handle collision with obstacles
    private void OnCollisionEnter2D(Collision2D collision)
    {
        // Check if the bird collides with an obstacle
        if (collision.gameObject.CompareTag("Obstacle"))
        {
            // End the game or trigger game over logic
            GameOver();
        }
    }

    // Method to handle game over logic
    void GameOver()
    {
        // Implement game over logic here
        Debug.Log("Game Over");
        // Optionally, you can stop the game or reset the scene
        // For example: SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }
}