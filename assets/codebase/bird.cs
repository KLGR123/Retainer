using UnityEngine;

public class Bird : MonoBehaviour
{
    // The force applied to the bird when the player taps the screen
    public float flapForce = 5f;
    // The gravity scale applied to the bird
    public float gravityScale = 1f;
    // The Rigidbody2D component attached to the bird
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

    // Apply an upward force to the bird
    void Flap()
    {
        // Reset the bird's vertical velocity
        rb.velocity = new Vector2(rb.velocity.x, 0);
        // Apply an upward force to the bird
        rb.AddForce(Vector2.up * flapForce, ForceMode2D.Impulse);
    }

    // This function is called when the bird collides with another collider
    void OnCollisionEnter2D(Collision2D collision)
    {
        // Check if the bird has collided with a pipe
        if (collision.gameObject.CompareTag("Pipe"))
        {
            // End the game
            GameOver();
        }
    }

    // End the game
    void GameOver()
    {
        // Log game over message
        Debug.Log("Game Over!");
        // Optionally, implement additional game over logic here
    }
}