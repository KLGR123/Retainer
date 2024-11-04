using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIControl : MonoBehaviour
{
    public Text scoreText;
    public Text gameOverText;

    void Start()
    {
        scoreText.text = "Score: 0";
        gameOverText.gameObject.SetActive(false);
    }

    public void UpdateScore(int score)
    {
        scoreText.text = "Score: " + score;
    }

    public void ShowGameOver()
    {
        gameOverText.gameObject.SetActive(true);
    }
}