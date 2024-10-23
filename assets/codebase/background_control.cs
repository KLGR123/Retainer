using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BackgroundControl : MonoBehaviour
{
    // Speed at which the background moves
    public float backgroundSpeed = 0.5f;
    // Reference to the Renderer component of the background
    private Renderer backgroundRenderer;

    void Start()
    {
        // Get the Renderer component attached to the background
        backgroundRenderer = GetComponent<Renderer>();
    }

    void Update()
    {
        // Calculate the new offset based on the speed and time
        float offset = Time.time * backgroundSpeed;
        // Set the texture offset to create a scrolling effect
        backgroundRenderer.material.mainTextureOffset = new Vector2(offset, 0);
    }
}