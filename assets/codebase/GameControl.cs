using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameControl : MonoBehaviour {

    public static GameControl instance;
    public Text scoreText;
    public Text comboText;
    public GameObject gameOverText;
    public bool gameOver = false;
    public float spawnRate = 2f;
    public GameObject slowBugPrefab;
    public GameObject fastBugPrefab;
    private int score = 0;
    private int combo = 0;
    private float timeSinceLastSpawned;
    private bool bigFootBuffActive = false;
    private float bigFootBuffDuration = 5f;
    private float bigFootBuffTimer = 0f;

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
        Time.timeScale = 0;
    }

    void Start()
    {
        UpdateScoreText();
        UpdateComboText();
    }

    void Update()
    {
        if (!gameOver)
        {
            timeSinceLastSpawned += Time.deltaTime;
            if (timeSinceLastSpawned >= spawnRate)
            {
                timeSinceLastSpawned = 0;
                SpawnBug();
            }

            if (bigFootBuffActive)
            {
                bigFootBuffTimer += Time.deltaTime;
                if (bigFootBuffTimer >= bigFootBuffDuration)
                {
                    DeactivateBigFootBuff();
                }
            }
        }
    }

    public void OnStartGame()
    {
        Time.timeScale = 1;
        gameOver = false;
        score = 0;
        combo = 0;
        UpdateScoreText();
        UpdateComboText();
    }

    public void OnGameOver()
    {
        gameOver = true;
        gameOverText.SetActive(true);
    }

    public void BugSquashed(int points)
    {
        if (gameOver)
        {
            return;
        }
        score += points;
        combo++;
        UpdateScoreText();
        UpdateComboText();

        if (combo >= 10 && !bigFootBuffActive)
        {
            ActivateBigFootBuff();
        }
    }

    public void ResetCombo()
    {
        combo = 0;
        UpdateComboText();
    }

    private void UpdateScoreText()
    {
        scoreText.text = "Score: " + score.ToString();
    }

    private void UpdateComboText()
    {
        comboText.text = "Combo: " + combo.ToString();
    }

    private void SpawnBug()
    {
        float spawnYPosition = Random.Range(-3f, 3f); // Adjust Y range based on your scene
        Vector2 spawnPosition = new Vector2(10f, spawnYPosition); // X position is fixed, Y is random

        float randomValue = Random.value;
        GameObject bugPrefab = randomValue < 0.7f ? slowBugPrefab : fastBugPrefab;

        Instantiate(bugPrefab, spawnPosition, Quaternion.identity);
    }

    private void ActivateBigFootBuff()
    {
        bigFootBuffActive = true;
        bigFootBuffTimer = 0f;
        FootControl.instance.ActivateBigFoot();
    }

    private void DeactivateBigFootBuff()
    {
        bigFootBuffActive = false;
        FootControl.instance.DeactivateBigFoot();
    }
}