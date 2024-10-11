using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameControl : MonoBehaviour
{
    public float moveSpeed = 5f; // 玩家移动速度
    public float riverSpeed = 2f; // 河流初始速度
    public float riverSpeedIncrease = 0.1f; // 河流速度增加量
    public float maxRiverSpeed = 5f; // 河流最大速度
    public float riverWidth = 10f; // 河道宽度
    public float riverNarrowRate = 0.05f; // 河道变窄速率
    public float minRiverWidth = 5f; // 河道最小宽度

    private float score = 0f; // 玩家得分
    private bool isGameOver = false; // 游戏结束标志

    void Update()
    {
        if (!isGameOver)
        {
            HandleMovement();
            UpdateRiver();
            CheckForGameOver();
        }
    }

    // 处理玩家左右移动
    void HandleMovement()
    {
        float horizontalInput = Input.GetAxis("Horizontal");
        Vector3 movement = new Vector3(horizontalInput * moveSpeed * Time.deltaTime, 0, 0);
        transform.Translate(movement);

        // 限制玩家在河道内移动
        float clampedX = Mathf.Clamp(transform.position.x, -riverWidth / 2, riverWidth / 2);
        transform.position = new Vector3(clampedX, transform.position.y, transform.position.z);
    }

    // 更新河流状态
    void UpdateRiver()
    {
        // 增加河流速度
        riverSpeed = Mathf.Min(riverSpeed + riverSpeedIncrease * Time.deltaTime, maxRiverSpeed);

        // 变窄河道
        riverWidth = Mathf.Max(riverWidth - riverNarrowRate * Time.deltaTime, minRiverWidth);

        // 更新得分
        score += riverSpeed * Time.deltaTime;
    }

    // 检查游戏结束条件
    void CheckForGameOver()
    {
        // 检查与障碍物的碰撞
        // 这里假设有一个方法 IsCollidingWithObstacle() 来检测碰撞
        if (IsCollidingWithObstacle())
        {
            isGameOver = true;
            Debug.Log("Game Over! Your score: " + score);
        }
    }

    // 假设的碰撞检测方法
    bool IsCollidingWithObstacle()
    {
        // 这里应该实现实际的碰撞检测逻辑
        return false;
    }
}