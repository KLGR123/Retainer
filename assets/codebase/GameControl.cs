using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameControl : MonoBehaviour
{
    public static GameControl instance;
    public GameObject fastBugPrefab;
    public GameObject slowBugPrefab;
    public Text scoreText;
    public Text gameOverText;
    public float spawnRate = 2f;
    public int maxMissedBugs = 5;

    private int score = 0;
    private int missedBugs = 0;
    private int consecutiveHits = 0;
    private bool gameOver = false;

    void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else if (instance != this)
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        StartCoroutine(SpawnBugs());
        gameOverText.gameObject.SetActive(false);
    }

    private IEnumerator SpawnBugs()
    {
        while (!gameOver)
        {
            float spawnXPosition = 10f;
            float spawnYPosition = Random.Range(-3f, 3f);
            GameObject bug = Random.value > 0.5f ? fastBugPrefab : slowBugPrefab;
            Instantiate(bug, new Vector3(spawnXPosition, spawnYPosition, 0), Quaternion.identity);
            yield return new WaitForSeconds(spawnRate);
        }
    }

    public void BugSquashed(bool isFastBug)
    {
        score += isFastBug ? 2 : 1;
        consecutiveHits++;
        if (consecutiveHits == 10)
        {
            score *= 2;
        }
        else if (consecutiveHits == 20)
        {
            FindObjectOfType<FootControl>().ActivateBigFootBuff();
        }
        scoreText.text = "Score: " + score;
    }

    public void MissedBug()
    {
        missedBugs++;
        if (missedBugs >= maxMissedBugs)
        {
            GameOver();
        }
    }

    private void GameOver()
    {
        gameOver = true;
        gameOverText.gameObject.SetActive(true);
        StopAllCoroutines();
    }
}