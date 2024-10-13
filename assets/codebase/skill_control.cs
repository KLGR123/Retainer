using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SkillControl : MonoBehaviour
{
    // Cooldown time for the skill in seconds
    private float skillCooldown = 3.0f;
    // Timer to track the cooldown
    private float skillTimer = 0.0f;
    // Boolean to check if the skill is ready to be used
    private bool isSkillReady = true;

    // Reference to the skill effect prefab
    public GameObject skillEffectPrefab;
    // Reference to the tower that will use the skill
    public GameObject tower;

    void Update()
    {
        // Update the skill timer
        if (!isSkillReady)
        {
            skillTimer += Time.deltaTime;
            if (skillTimer >= skillCooldown)
            {
                isSkillReady = true;
                skillTimer = 0.0f;
            }
        }

        // Check for player input to activate the skill
        if (Input.GetKeyDown(KeyCode.Space) && isSkillReady)
        {
            ActivateSkill();
        }
    }

    // Method to activate the skill
    private void ActivateSkill()
    {
        // Instantiate the skill effect at the tower's position
        Instantiate(skillEffectPrefab, tower.transform.position, Quaternion.identity);
        // Set the skill as not ready
        isSkillReady = false;
        // Logic to clear enemies in range can be added here
        ClearEnemiesInRange();
    }

    // Method to clear enemies in range
    private void ClearEnemiesInRange()
    {
        // Define the range of the skill effect
        float skillRange = 5.0f;
        // Find all enemies within the range
        Collider[] hitColliders = Physics.OverlapSphere(tower.transform.position, skillRange);
        foreach (var hitCollider in hitColliders)
        {
            if (hitCollider.CompareTag("Enemy"))
            {
                // Destroy the enemy
                Destroy(hitCollider.gameObject);
            }
        }
    }
}