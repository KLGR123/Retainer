using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Enum to define different item types
public enum ItemType
{
    Gold,
    Stone,
    Diamond,
    HealthPotion, // New item type for health potion
    SpeedBoost    // New item type for speed boost
}

// Base class for all items
public class Item : MonoBehaviour
{
    public ItemType itemType;
    public int points;
    public float pullSpeed;

    // Method to initialize item properties based on type
    public void Initialize(ItemType type)
    {
        itemType = type;
        switch (itemType)
        {
            case ItemType.Gold:
                points = 100; // Normal points for gold
                pullSpeed = 1.0f; // Normal speed for gold
                break;
            case ItemType.Stone:
                points = 50; // Fewer points for stone
                pullSpeed = 0.5f; // Slower speed for stone
                break;
            case ItemType.Diamond:
                points = 200; // More points for diamond
                pullSpeed = 1.5f; // Faster speed for diamond
                break;
            case ItemType.HealthPotion:
                points = 0; // No points for health potion
                pullSpeed = 1.0f; // Normal speed for health potion
                break;
            case ItemType.SpeedBoost:
                points = 0; // No points for speed boost
                pullSpeed = 1.0f; // Normal speed for speed boost
                break;
        }
    }
}

// Class to control the item behavior
public class ItemControl : MonoBehaviour
{
    public List<Item> items; // List to hold all items in the game

    // Method to simulate the hook grabbing an item
    public void GrabItem(Item item)
    {
        StartCoroutine(PullItem(item));
    }

    // Coroutine to pull the item back to the player
    private IEnumerator PullItem(Item item)
    {
        Vector3 startPosition = item.transform.position;
        Vector3 endPosition = transform.position; // Assuming the player is at the transform position

        float journey = 0f;
        while (journey <= 1f)
        {
            journey += Time.deltaTime * item.pullSpeed;
            item.transform.position = Vector3.Lerp(startPosition, endPosition, journey);
            yield return null;
        }

        // Once the item is pulled back, process the item effect
        ProcessItemEffect(item);
        Destroy(item.gameObject); // Remove the item from the scene
    }

    // Method to process the effect of the item
    private void ProcessItemEffect(Item item)
    {
        switch (item.itemType)
        {
            case ItemType.Gold:
            case ItemType.Stone:
            case ItemType.Diamond:
                AddPoints(item.points);
                break;
            case ItemType.HealthPotion:
                // Assuming there's a Player class handling health
                Player.Instance.IncreaseHealth(20); // Increase player's health by 20
                break;
            case ItemType.SpeedBoost:
                // Assuming there's a Player class handling speed
                StartCoroutine(Player.Instance.ActivateSpeedBoost(5.0f, 10.0f)); // Boost speed by 5 for 10 seconds
                break;
        }
    }

    // Method to add points to the player's score
    private void AddPoints(int points)
    {
        // Assuming there's a GameManager class handling the score
        GameManager.Instance.AddScore(points);
    }
}