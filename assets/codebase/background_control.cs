using UnityEngine;

public class BackgroundControl : MonoBehaviour
{
    // Reference to the background image or object
    public GameObject background;

    // Speed at which the background scrolls
    public float scrollSpeed = 0.1f;

    // Offset value to create a seamless loop
    private Vector2 offset;

    // Reference to the material of the background
    private Material backgroundMaterial;

    void Start()
    {
        // Get the material of the background object
        if (background != null)
        {
            backgroundMaterial = background.GetComponent<Renderer>().material;
        }
        else
        {
            Debug.LogError("Background object is not assigned.");
        }
    }

    void Update()
    {
        // Calculate the new offset based on the scroll speed and time
        offset = new Vector2(Time.time * scrollSpeed, 0);

        // Apply the offset to the material to create a scrolling effect
        if (backgroundMaterial != null)
        {
            backgroundMaterial.mainTextureOffset = offset;
        }
    }

    // Method to change the background dynamically
    public void ChangeBackground(GameObject newBackground)
    {
        if (newBackground != null)
        {
            background = newBackground;
            backgroundMaterial = background.GetComponent<Renderer>().material;
        }
        else
        {
            Debug.LogError("New background object is not assigned.");
        }
    }

    // Method to adjust the scroll speed dynamically
    public void SetScrollSpeed(float newScrollSpeed)
    {
        scrollSpeed = newScrollSpeed;
    }
}