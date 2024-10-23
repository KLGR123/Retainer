using UnityEngine;
using UnityEngine.UI;

public class UIControl : MonoBehaviour
{
    // Reference to the Text component for displaying the countdown timer
    public Text countdownText;
    // Reference to the Text component for displaying the current score
    public Text scoreText;
    // Reference to the GameObject for the game over panel
    public GameObject gameOverPanel;
    // Reference to the Text component for displaying the final score on the game over panel
    public Text finalScoreText;
    // Reference to the Button component for restarting the game
    public Button restartButton;

    // Total game time in seconds
    private float totalTime = 60f;
    // Current score of the player
    private int currentScore = 0;
    // Timer to keep track of the countdown
    private float timer;

    void Start()
    {
        // Initialize the timer with the total game time
        timer = totalTime;
        // Update the score display at the start
        UpdateScoreDisplay();
        // Hide the game over panel at the start
        gameOverPanel.SetActive(false);
        // Add listener to the restart button
        restartButton.onClick.AddListener(RestartGame);
    }

    void Update()
    {
        // Update the countdown timer every frame
        UpdateCountdownTimer();
    }

    // Method to update the countdown timer
    private void UpdateCountdownTimer()
    {
        // Decrease the timer by the time passed since the last frame
        timer -= Time.deltaTime;

        // If the timer reaches zero, end the game
        if (timer <= 0)
        {
            timer = 0;
            EndGame();
        }

        // Update the countdown text display
        countdownText.text = "Time: " + Mathf.Ceil(timer).ToString();
    }

    // Method to update the score display
    public void UpdateScoreDisplay()
    {
        // Update the score text display
        scoreText.text = "Score: " + currentScore.ToString();
    }

    // Method to add points to the current score
    public void AddScore(int points)
    {
        // Increase the current score by the given points
        currentScore += points;
        // Update the score display
        UpdateScoreDisplay();
    }

    // Method to handle the end of the game
    private void EndGame()
    {
        // Display a message or handle the end of the game logic
        Debug.Log("Game Over! Final Score: " + currentScore);
        // Show the game over panel
        gameOverPanel.SetActive(true);
        // Update the final score text on the game over panel
        finalScoreText.text = "Final Score: " + currentScore.ToString();
    }

    // Method to restart the game
    private void RestartGame()
    {
        // Reset the timer
        timer = totalTime;
        // Reset the score
        currentScore = 0;
        // Update the score display
        UpdateScoreDisplay();
        // Hide the game over panel
        gameOverPanel.SetActive(false);
        // Additional logic to reset the game state can be added here
        Debug.Log("Game Restarted");
    }
}