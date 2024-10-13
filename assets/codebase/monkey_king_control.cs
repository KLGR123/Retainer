using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MonkeyKingControl : MonoBehaviour
{
    public float moveSpeed = 5f; // 移动速度
    public float grabRange = 2f; // 抓取范围
    public int score = 0; // 当前得分

    private Rigidbody2D rb;
    private Vector2 movement;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        ProcessInputs();
    }

    void FixedUpdate()
    {
        Move();
    }

    // 处理玩家输入
    void ProcessInputs()
    {
        float moveX = Input.GetAxis("Horizontal");
        float moveY = Input.GetAxis("Vertical");
        movement = new Vector2(moveX, moveY).normalized;
        
        if (Input.GetKeyDown(KeyCode.Space))
        {
            TryGrabMonster();
        }
    }

    // 移动齐天大圣
    void Move()
    {
        rb.velocity = movement * moveSpeed;
    }

    // 尝试抓取妖怪
    void TryGrabMonster()
    {
        Collider2D[] hitColliders = Physics2D.OverlapCircleAll(transform.position, grabRange);
        foreach (var hitCollider in hitColliders)
        {
            if (hitCollider.CompareTag("Monster"))
            {
                GrabMonster(hitCollider.gameObject);
                break; // 每次只抓一个妖怪
            }
        }
    }

    // 抓取妖怪并增加分数
    void GrabMonster(GameObject monster)
    {
        Monster monsterScript = monster.GetComponent<Monster>();
        if (monsterScript != null)
        {
            score += monsterScript.GetScore();
            Destroy(monster); // 抓到后销毁妖怪
        }
    }

    // 可视化抓取范围（仅在编辑器中可见）
    void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, grabRange);
    }
}

// 妖怪类，负责提供分数
public class Monster : MonoBehaviour
{
    public int scoreValue = 10; // 默认分数

    // 获取妖怪的分数
    public int GetScore()
    {
        return scoreValue;
    }
}