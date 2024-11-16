using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIControl : MonoBehaviour {

    public Text scoreText;
    public Text timerText;
    public GameObject gameOverPanel;

    void Start()
    {
        gameOverPanel.SetActive(false);
    }

    public void UpdateScore(int score)
    {
        scoreText.text = "Score: " + score.ToString();
    }

    public void UpdateTimer(float timeRemaining)
    {
        timerText.text = "Time: " + Mathf.Ceil(timeRemaining).ToString();
    }

    public void ShowGameOver()
    {
        gameOverPanel.SetActive(true);
    }
}