using UnityEngine;

public class GoldControl : MonoBehaviour
{
    // 金矿的价值
    public int value = 10;

    // 金矿被抓取时的处理
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.gameObject.CompareTag('Miner'))
        {
            // 增加玩家的得分
            other.gameObject.GetComponent<MinerControl>().AddScore(value);
            // 销毁金矿
            Destroy(gameObject);
        }
    }
}