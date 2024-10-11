using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RiverControl : MonoBehaviour
{
    // Speed of the river flow
    public float riverSpeed = 3.0f; // Lowered initial speed from 5.0f to 3.0f
    // Minimum and maximum speed of the river
    public float minRiverSpeed = 2.0f;
    public float maxRiverSpeed = 10.0f;
    // Width of the river
    public float riverWidth = 10.0f;
    // Minimum and maximum width of the river
    public float minRiverWidth = 5.0f;
    public float maxRiverWidth = 15.0f;

    // Reference to the player character
    public GameObject player;

    // Update is called once per frame
    void Update()
    {
        // Update the river's speed and width over time or based on game events
        UpdateRiverProperties();

        // Move the player along with the river flow
        MovePlayerWithRiver();
    }

    // Function to update river properties like speed and width
    void UpdateRiverProperties()
    {
        // Example logic to change river speed and width
        // This can be replaced with more complex logic based on game design
        riverSpeed = Mathf.Clamp(riverSpeed + Time.deltaTime * 0.1f, minRiverSpeed, maxRiverSpeed);
        riverWidth = Mathf.Clamp(riverWidth + Mathf.Sin(Time.time) * 0.1f, minRiverWidth, maxRiverWidth);
    }

    // Function to move the player with the river flow
    void MovePlayerWithRiver()
    {
        if (player != null)
        {
            // Move the player downstream with the river's speed
            player.transform.Translate(Vector3.forward * riverSpeed * Time.deltaTime);

            // Allow player to move left and right within the river's width
            float horizontalInput = Input.GetAxis("Horizontal");
            player.transform.Translate(Vector3.right * horizontalInput * riverWidth * Time.deltaTime);
        }
    }
}