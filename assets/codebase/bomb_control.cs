using UnityEngine;

public class BombControl : MonoBehaviour
{
    // 炸弹的伤害值
    public int damage = 10;

    // 炸弹被抓取时的处理
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.gameObject.CompareTag('Miner'))
        {
            // 减少玩家的得分
            other.gameObject.GetComponent<MinerControl>().AddScore(-damage);
            // 销毁炸弹
            Destroy(gameObject);
        }
    }
}