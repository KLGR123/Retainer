using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MonsterControl : MonoBehaviour
{
    public GameObject bigMonsterPrefab; // 大妖怪的预制体
    public GameObject smallMonsterPrefab; // 小妖怪的预制体
    public int bigMonsterScore = 10; // 大妖怪的分数
    public int smallMonsterScore = 5; // 小妖怪的分数
    public float spawnInterval = 3.0f; // 妖怪生成的时间间隔
    public float moveSpeed = 2.0f; // 妖怪的移动速度
    public Transform[] spawnPoints; // 妖怪生成的地点

    private List<GameObject> monsters = new List<GameObject>(); // 当前场景中的妖怪列表
    private int score = 0; // 玩家当前的分数

    void Start()
    {
        // 开始生成妖怪的协程
        StartCoroutine(SpawnMonsters());
    }

    void Update()
    {
        // 更新妖怪的移动
        MoveMonsters();
    }

    IEnumerator SpawnMonsters()
    {
        while (true)
        {
            // 随机选择生成大妖怪还是小妖怪
            bool spawnBigMonster = Random.value > 0.5f;
            GameObject monsterPrefab = spawnBigMonster ? bigMonsterPrefab : smallMonsterPrefab;

            // 随机选择一个生成点
            Transform spawnPoint = spawnPoints[Random.Range(0, spawnPoints.Length)];

            // 生成妖怪
            GameObject monster = Instantiate(monsterPrefab, spawnPoint.position, spawnPoint.rotation);
            monsters.Add(monster);

            // 等待一段时间后再生成下一个妖怪
            yield return new WaitForSeconds(spawnInterval);
        }
    }

    void MoveMonsters()
    {
        foreach (GameObject monster in monsters)
        {
            if (monster != null)
            {
                // 妖怪向下移动
                monster.transform.Translate(Vector3.down * moveSpeed * Time.deltaTime);
            }
        }
    }

    public void CatchMonster(GameObject monster)
    {
        if (monsters.Contains(monster))
        {
            // 根据妖怪类型增加分数
            if (monster.CompareTag("BigMonster"))
            {
                score += bigMonsterScore;
            }
            else if (monster.CompareTag("SmallMonster"))
            {
                score += smallMonsterScore;
            }

            // 移除妖怪
            monsters.Remove(monster);
            Destroy(monster);

            // 更新分数显示（假设有一个 UI 管理器来处理分数显示）
            UIManager.Instance.UpdateScore(score);
        }
    }
}