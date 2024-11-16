using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameControl : MonoBehaviour {

    public static GameControl instance;
    public Text scoreText;
    public Text timerText;
    public GameObject gameOverText;
    public int score = 0;
    public float gameTime = 60f; // Total game time in seconds
    private float timeRemaining;
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
        timeRemaining = gameTime;
    }

    void Start()
    {
        UpdateScoreText();
        UpdateTimerText();
    }

    void Update()
    {
        if (!gameOver)
        {
            timeRemaining -= Time.deltaTime;
            UpdateTimerText();

            if (timeRemaining <= 0)
            {
                EndGame();
            }
        }
    }

    public void MoleHit()
    {
        if (!gameOver)
        {
            score++;
            UpdateScoreText();
        }
    }

    void UpdateScoreText()
    {
        scoreText.text = "Score: " + score.ToString();
    }

    void UpdateTimerText()
    {
        timerText.text = "Time: " + Mathf.Ceil(timeRemaining).ToString();
    }

    void EndGame()
    {
        gameOver = true;
        gameOverText.SetActive(true);
        // Logic to determine if the player advances to the next level or ends the game
    }
}