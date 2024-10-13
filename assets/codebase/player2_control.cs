using UnityEngine;

public class Player2Control : MonoBehaviour
{
    // 钩爪的速度
    public float clawSpeed = 5.0f;
    // 钩爪的最大距离
    public float maxDistance = 10.0f;
    // 钩爪的当前状态
    private enum ClawState { Idle, Swinging, Retracting }
    private ClawState currentState = ClawState.Idle;

    // 钩爪的起始位置
    private Vector3 startPosition;
    // 钩爪的目标位置
    private Vector3 targetPosition;
    // 钩爪的当前方向
    private Vector3 direction;

    // 玩家2的分数
    private int score = 0;

    // 钩爪的抓取对象
    private GameObject grabbedObject;

    void Start()
    {
        // 初始化钩爪的起始位置
        startPosition = transform.position;
    }

    void Update()
    {
        // 检测玩家输入
        if (Input.GetMouseButtonDown(1)) // 右键点击触发
        {
            if (currentState == ClawState.Idle)
            {
                // 计算目标位置
                Vector3 mousePosition = Input.mousePosition;
                mousePosition.z = Camera.main.nearClipPlane;
                targetPosition = Camera.main.ScreenToWorldPoint(mousePosition);
                direction = (targetPosition - startPosition).normalized;
                currentState = ClawState.Swinging;
            }
        }

        // 更新钩爪状态
        switch (currentState)
        {
            case ClawState.Swinging:
                SwingClaw();
                break;
            case ClawState.Retracting:
                RetractClaw();
                break;
        }
    }

    void SwingClaw()
    {
        // 钩爪向目标位置移动
        transform.position += direction * clawSpeed * Time.deltaTime;

        // 检查钩爪是否到达最大距离
        if (Vector3.Distance(startPosition, transform.position) >= maxDistance)
        {
            currentState = ClawState.Retracting;
        }
    }

    void RetractClaw()
    {
        // 钩爪返回起始位置
        transform.position = Vector3.MoveTowards(transform.position, startPosition, clawSpeed * Time.deltaTime);

        // 检查钩爪是否返回到起始位置
        if (Vector3.Distance(transform.position, startPosition) < 0.1f)
        {
            currentState = ClawState.Idle;
            if (grabbedObject != null)
            {
                // 结算分数
                CalculateScore(grabbedObject);
                Destroy(grabbedObject);
                grabbedObject = null;
            }
        }
    }

    void OnTriggerEnter(Collider other)
    {
        if (currentState == ClawState.Swinging)
        {
            // 钩爪抓取物品
            grabbedObject = other.gameObject;
            currentState = ClawState.Retracting;
        }
    }

    void CalculateScore(GameObject obj)
    {
        // 根据物品类型结算分数
        switch (obj.tag)
        {
            case "Gold":
                score += 10; // 假设金矿得10分
                break;
            case "Stone":
                score += 2; // 假设石头得2分
                break;
            case "Diamond":
                score += 20; // 假设钻石得20分
                break;
        }
    }
}