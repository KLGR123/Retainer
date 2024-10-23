using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// 定义物品的基类
public abstract class Item : MonoBehaviour
{
    public int points; // 物品的积分
    public float pullSpeed; // 抓回的速度

    // 抓取物品时调用的方法
    public abstract void OnGrab();
}

// 金矿类，继承自Item
public class Gold : Item
{
    // 构造函数，初始化金矿的属性
    public Gold()
    {
        // 金矿的积分和抓回速度
        points = 100; // 正常积分
        pullSpeed = 1.0f; // 正常速度
    }

    // 抓取金矿时调用的方法
    public override void OnGrab()
    {
        // 这里可以实现抓取金矿时的特效或音效
        Debug.Log("Gold grabbed! Points: " + points);
    }
}

// 石头类，继承自Item
public class Rock : Item
{
    // 构造函数，初始化石头的属性
    public Rock()
    {
        // 石头的积分和抓回速度
        points = 15; // 修改为15
        pullSpeed = 0.5f; // 缓慢速度
    }

    // 抓取石头时调用的方法
    public override void OnGrab()
    {
        // 这里可以实现抓取石头时的特效或音效
        Debug.Log("Rock grabbed! Points: " + points);
    }
}

// 新的道具类，继承自Item
public class PowerUp : Item
{
    private float duration = 5.0f; // 增加积分的持续时间

    // 构造函数，初始化道具的属性
    public PowerUp()
    {
        // 道具的积分和抓回速度
        points = 50; // 短暂增加的积分
        pullSpeed = 1.2f; // 略快的速度
    }

    // 抓取道具时调用的方法
    public override void OnGrab()
    {
        // 这里可以实现抓取道具时的特效或音效
        Debug.Log("PowerUp grabbed! Temporary Points: " + points);
        // 启动协程来处理短暂增加积分的效果
        ScoreManager.Instance.StartCoroutine(TemporaryScoreBoost());
    }

    // 协程：短暂增加积分
    private IEnumerator TemporaryScoreBoost()
    {
        ScoreManager.Instance.AddScore(points);
        yield return new WaitForSeconds(duration);
        ScoreManager.Instance.AddScore(-points);
    }
}

// 物品控制器类
public class ItemController : MonoBehaviour
{
    public List<Item> items; // 场景中的所有物品

    // 初始化物品
    void Start()
    {
        items = new List<Item>();

        // 生成一些金矿和石头
        for (int i = 0; i < 5; i++)
        {
            // 创建金矿
            GameObject goldObject = new GameObject("Gold");
            Gold gold = goldObject.AddComponent<Gold>();
            items.Add(gold);

            // 创建石头
            GameObject rockObject = new GameObject("Rock");
            Rock rock = rockObject.AddComponent<Rock>();
            items.Add(rock);

            // 创建道具
            GameObject powerUpObject = new GameObject("PowerUp");
            PowerUp powerUp = powerUpObject.AddComponent<PowerUp>();
            items.Add(powerUp);
        }
    }

    // 更新物品状态
    void Update()
    {
        // 这里可以实现物品的动态行为，比如移动或旋转
    }

    // 当挖掘工具抓到物品时调用
    public void GrabItem(Item item)
    {
        item.OnGrab();
        // 根据物品类型和属性处理游戏逻辑，比如增加积分
        // 假设有一个积分管理器来处理积分
        ScoreManager.Instance.AddScore(item.points);

        // 处理抓回速度
        StartCoroutine(PullItemBack(item));
    }

    // 协程：处理物品的抓回
    private IEnumerator PullItemBack(Item item)
    {
        // 这里可以实现物品被抓回的动画或效果
        float pullDuration = 1.0f / item.pullSpeed; // 根据抓回速度计算时间
        float elapsedTime = 0f;

        Vector3 startPosition = item.transform.position;
        Vector3 endPosition = transform.position; // 假设抓回到控制器的位置

        while (elapsedTime < pullDuration)
        {
            item.transform.position = Vector3.Lerp(startPosition, endPosition, (elapsedTime / pullDuration));
            elapsedTime += Time.deltaTime;
            yield return null;
        }

        // 抓回完成后，销毁物品
        Destroy(item.gameObject);
    }
}