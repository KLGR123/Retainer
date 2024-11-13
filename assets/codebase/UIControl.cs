using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIControl : MonoBehaviour {

    public Text scoreText;
    public Text comboText;
    public Text buffText;
    public GameObject startButton;
    public GameObject gameOverText;

    void Start()
    {
        startButton.SetActive(true);
        gameOverText.SetActive(false);
        buffText.gameObject.SetActive(false);
    }

    public void OnStartButton()
    {
        startButton.SetActive(false);
        gameOverText.SetActive(false);
        GameControl.instance.OnStartGame();
    }

    public void UpdateScore(int score)
    {
        scoreText.text = "Score: " + score.ToString();
    }

    public void UpdateCombo(int combo)
    {
        comboText.text = "Combo: " + combo.ToString();
    }

    public void ShowGameOver()
    {
        gameOverText.SetActive(true);
    }

    public void ShowBuffStatus(bool isActive)
    {
        buffText.gameObject.SetActive(isActive);
        if (isActive)
        {
            buffText.text = "Big Foot Active!";
        }
    }
}