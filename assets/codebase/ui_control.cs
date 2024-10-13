using UnityEngine;
using UnityEngine.UI;

public class UIControl : MonoBehaviour
{
    // UI Elements
    public Text scoreText;
    public Text timerText;
    public Button startButton;
    public GameObject gameOverPanel;
    public Text gameOverScoreText;

    // Game variables
    private int score;
    private float timer;
    private bool isGameActive;

    void Start()
    {
        // Initialize game state
        score = 0;
        timer = 60.0f; // 60 seconds for the game
        isGameActive = false;

        // Set up UI
        UpdateScoreText();
        UpdateTimerText();
        gameOverPanel.SetActive(false);

        // Add listener to start button
        startButton.onClick.AddListener(StartGame);
    }

    void Update()
    {
        if (isGameActive)
        {
            // Update timer
            timer -= Time.deltaTime;
            UpdateTimerText();

            // Check if time is up
            if (timer <= 0)
            {
                EndGame();
            }
        }
    }

    void StartGame()
    {
        // Reset game state
        score = 0;
        timer = 60.0f;
        isGameActive = true;

        // Update UI
        UpdateScoreText();
        UpdateTimerText();
        gameOverPanel.SetActive(false);
    }

    void EndGame()
    {
        isGameActive = false;
        gameOverPanel.SetActive(true);
        gameOverScoreText.text = "Score: " + score;
    }

    public void AddScore(int points)
    {
        if (isGameActive)
        {
            score += points;
            UpdateScoreText();
        }
    }

    void UpdateScoreText()
    {
        scoreText.text = "Score: " + score;
    }

    void UpdateTimerText()
    {
        timerText.text = "Time: " + Mathf.Ceil(timer);
    }
}