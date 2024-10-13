using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LuckyCloverControl : MonoBehaviour
{
    // Duration for which the lucky clover effect lasts
    public float effectDuration = 5.0f;

    // Reference to the player controllers to apply the effect
    public PlayerController player1;
    public PlayerController player2;

    // Flag to check if the clover is active
    private bool isActive = false;

    // Start is called before the first frame update
    void Start()
    {
        // Initialize any necessary components or variables
    }

    // Update is called once per frame
    void Update()
    {
        // Handle any updates related to the lucky clover
    }

    // Method to handle collision with the player's claw
    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player1Claw") || other.CompareTag("Player2Claw"))
        {
            if (!isActive)
            {
                isActive = true;
                StartCoroutine(ApplyLuckyCloverEffect(other));
            }
        }
    }

    // Coroutine to apply the lucky clover effect
    private IEnumerator ApplyLuckyCloverEffect(Collider2D playerClaw)
    {
        PlayerController player = null;

        // Determine which player collected the clover
        if (playerClaw.CompareTag("Player1Claw"))
        {
            player = player1;
        }
        else if (playerClaw.CompareTag("Player2Claw"))
        {
            player = player2;
        }

        if (player != null)
        {
            // Increase the player's claw speed
            player.IncreaseClawSpeed();

            // Wait for the effect duration
            yield return new WaitForSeconds(effectDuration);

            // Reset the player's claw speed
            player.ResetClawSpeed();
        }

        // Deactivate the clover
        isActive = false;

        // Optionally, destroy the clover object after use
        Destroy(gameObject);
    }
}