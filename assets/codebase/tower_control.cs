using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// 定义塔的基本属性和行为
public class Tower : MonoBehaviour
{
    public float range = 5.0f; // 塔的攻击范围
    public float fireRate = 1.0f; // 塔的攻击速度
    public int damage = 10; // 塔的攻击伤害
    public float skillCooldown = 3.0f; // 技能冷却时间
    private float skillCooldownTimer = 0.0f; // 技能冷却计时器

    private Transform target; // 当前攻击目标
    private float fireCountdown = 0f; // 攻击计时器

    // 初始化塔
    void Start()
    {
        InvokeRepeating("UpdateTarget", 0f, 0.5f);
    }

    // 更新目标
    void UpdateTarget()
    {
        GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");
        float shortestDistance = Mathf.Infinity;
        GameObject nearestEnemy = null;

        foreach (GameObject enemy in enemies)
        {
            float distanceToEnemy = Vector3.Distance(transform.position, enemy.transform.position);
            if (distanceToEnemy < shortestDistance)
            {
                shortestDistance = distanceToEnemy;
                nearestEnemy = enemy;
            }
        }

        if (nearestEnemy != null && shortestDistance <= range)
        {
            target = nearestEnemy.transform;
        }
        else
        {
            target = null;
        }
    }

    // 更新塔的状态
    void Update()
    {
        if (target == null)
            return;

        if (fireCountdown <= 0f)
        {
            Shoot();
            fireCountdown = 1f / fireRate;
        }

        fireCountdown -= Time.deltaTime;

        // 更新技能冷却计时器
        if (skillCooldownTimer > 0)
        {
            skillCooldownTimer -= Time.deltaTime;
        }
    }

    // 塔的攻击行为
    void Shoot()
    {
        // 实现攻击逻辑，例如发射子弹
        Debug.Log("Shooting at " + target.name);
    }

    // 释放技能
    public void UseSkill()
    {
        if (skillCooldownTimer <= 0)
        {
            // 实现技能效果，例如清除大片敌人
            Debug.Log("Skill used!");

            // 重置技能冷却计时器
            skillCooldownTimer = skillCooldown;
        }
        else
        {
            Debug.Log("Skill is on cooldown. Time remaining: " + skillCooldownTimer);
        }
    }
}