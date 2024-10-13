using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameControl : MonoBehaviour
{
    public float countdownTime = 60f; // Game countdown timer
    private float currentTime;
    public int score = 0; // Player's score
    public int scoreToAdvance = 100; // Score needed to advance to the next level

    public GameObject hook; // Reference to the hook GameObject
    private bool isHookMoving = false; // Is the hook currently moving
    private Vector3 hookStartPosition; // Initial position of the hook

    public List<GameObject> towers; // List of towers placed by the player
    public List<GameObject> enemies; // List of enemies in the game
    public float skillCooldown = 3f; // Cooldown time for tower skills
    private float skillTimer = 0f; // Timer to track skill cooldown

    void Start()
    {
        currentTime = countdownTime;
        hookStartPosition = hook.transform.position;
    }

    void Update()
    {
        HandleInput();
        UpdateTimer();
        UpdateSkillCooldown();
        ManageEnemies();
    }

    // Handle player input
    void HandleInput()
    {
        if (Input.GetMouseButtonDown(0) && !isHookMoving)
        {
            // Start the hook movement
            StartCoroutine(MoveHook());
        }

        if (Input.GetKeyDown(KeyCode.Space) && skillTimer <= 0f)
        {
            // Activate tower skills
            ActivateTowerSkills();
            skillTimer = skillCooldown;
        }
    }

    // Update the game timer
    void UpdateTimer()
    {
        if (currentTime > 0)
        {
            currentTime -= Time.deltaTime;
        }
        else
        {
            EndGame();
        }
    }

    // Update the skill cooldown timer
    void UpdateSkillCooldown()
    {
        if (skillTimer > 0)
        {
            skillTimer -= Time.deltaTime;
        }
    }

    // Coroutine to move the hook
    IEnumerator MoveHook()
    {
        isHookMoving = true;
        Vector3 targetPosition = hookStartPosition + new Vector3(0, -5, 0); // Example target position

        // Move the hook downwards
        while (hook.transform.position != targetPosition)
        {
            hook.transform.position = Vector3.MoveTowards(hook.transform.position, targetPosition, Time.deltaTime * 5);
            yield return null;
        }

        // Simulate grabbing an item
        GameObject grabbedItem = SimulateGrabItem();

        // Move the hook back to the start position
        while (hook.transform.position != hookStartPosition)
        {
            hook.transform.position = Vector3.MoveTowards(hook.transform.position, hookStartPosition, Time.deltaTime * 5);
            yield return null;
        }

        // Process the grabbed item
        if (grabbedItem != null)
        {
            ProcessItem(grabbedItem);
        }

        isHookMoving = false;
    }

    // Simulate grabbing an item
    GameObject SimulateGrabItem()
    {
        // This is a placeholder for actual collision detection logic
        // In a real game, you would detect collision with items here
        return null;
    }

    // Process the grabbed item
    void ProcessItem(GameObject item)
    {
        // Determine item type and update score and hook speed accordingly
        string itemType = item.tag; // Assuming items are tagged appropriately

        switch (itemType)
        {
            case "Gold":
                score += 10; // Normal score
                break;
            case "Stone":
                score += 2; // Low score
                break;
            case "Diamond":
                score += 20; // High score
                break;
        }
    }

    // End the game
    void EndGame()
    {
        // Check if the player has enough score to advance
        if (score >= scoreToAdvance)
        {
            Debug.Log("Level Complete! Advancing to the next level.");
            // Logic to advance to the next level
        }
        else
        {
            Debug.Log("Game Over! Try again.");
            // Logic to end the game
        }
    }

    // Activate skills for all towers
    void ActivateTowerSkills()
    {
        foreach (GameObject tower in towers)
        {
            Tower towerComponent = tower.GetComponent<Tower>();
            if (towerComponent != null)
            {
                towerComponent.ActivateSkill();
            }
        }
    }

    // Manage enemies in the game
    void ManageEnemies()
    {
        foreach (GameObject enemy in enemies)
        {
            Enemy enemyComponent = enemy.GetComponent<Enemy>();
            if (enemyComponent != null)
            {
                enemyComponent.Move();
                if (enemyComponent.HasReachedGoal())
                {
                    EndGame();
                }
            }
        }
    }
}

// Example Tower class
public class Tower : MonoBehaviour
{
    public void ActivateSkill()
    {
        // Logic to activate the tower's skill
        Debug.Log("Tower skill activated!");
        // Example: Clear a large area of enemies
    }
}

// Example Enemy class
public class Enemy : MonoBehaviour
{
    public void Move()
    {
        // Logic for enemy movement
    }

    public bool HasReachedGoal()
    {
        // Logic to determine if the enemy has reached the goal
        return false;
    }
}