using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameControl : MonoBehaviour {

    public static GameControl instance;
    public GameObject gameOverText;
    public Text scoreText;
    public float gameDuration = 60f; // Game duration in seconds
    public bool gameOver = false;
    private float timeRemaining;
    private int score = 0;

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
        timeRemaining = gameDuration;
        Time.timeScale = 1;
    }

    void Update()
    {
        if (!gameOver)
        {
            timeRemaining -= Time.deltaTime;
            if (timeRemaining <= 0)
            {
                EndGame();
            }
        }
    }

    public void BugSquashed(int points)
    {
        if (gameOver)
        {
            return;
        }
        score += points;
        scoreText.text = "Score: " + score.ToString();
    }

    private void EndGame()
    {
        gameOver = true;
        gameOverText.SetActive(true);
        // Additional logic to evaluate player's performance based on score
    }
}