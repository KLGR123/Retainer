using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarrotControl : MonoBehaviour
{
    // Health of the carrot
    public int health = 100;

    // Reference to the game manager to update game state
    private GameManager gameManager;

    // Start is called before the first frame update
    void Start()
    {
        // Find the GameManager in the scene
        gameManager = FindObjectOfType<GameManager>();
    }

    // Method to reduce health of the carrot
    public void TakeDamage(int damage)
    {
        health -= damage;
        Debug.Log("Carrot took damage, current health: " + health);

        // Check if the carrot's health has reached zero
        if (health <= 0)
        {
            // Call the method to handle the carrot's destruction
            OnCarrotDestroyed();
        }
    }

    // Method to handle the carrot's destruction
    private void OnCarrotDestroyed()
    {
        Debug.Log("Carrot has been destroyed!");
        // Notify the game manager that the carrot has been destroyed
        gameManager.OnCarrotDestroyed();
    }

    // Method to heal the carrot
    public void Heal(int amount)
    {
        health += amount;
        Debug.Log("Carrot healed, current health: " + health);
    }
}