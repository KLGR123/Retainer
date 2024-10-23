using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class GameControl : MonoBehaviour
{
    public Text timerText;
    public Text scoreText;
    public int scoreToAdvance = 100; // Score required to advance to the next level
    public float gameDuration = 60f; // Game duration in seconds
    public GameObject bird; // Reference to the bird GameObject
    public float birdJumpForce = 5f; // Force applied to the bird when jumping
    public GameObject pipePrefab; // Reference to the pipe prefab
    public float pipeSpawnInterval = 2f; // Interval between pipe spawns
    public float pipeSpeed = 2f; // Speed at which pipes move

    private float timeRemaining;
    private int currentScore;
    private bool gameEnded;
    private Rigidbody2D birdRigidbody;

    void Start()
    {
        timeRemaining = gameDuration;
        currentScore = 0;
        gameEnded = false;
        birdRigidbody = bird.GetComponent<Rigidbody2D>();
        UpdateScoreText();
        StartCoroutine(GameTimer());
        StartCoroutine(SpawnPipes());
    }

    void Update()
    {
        if (gameEnded)
        {
            return;
        }

        // Handle player input for bird jump
        if (Input.GetMouseButtonDown(0))
        {
            BirdJump();
        }
    }

    private void BirdJump()
    {
        birdRigidbody.velocity = Vector2.up * birdJumpForce;
    }

    private IEnumerator GameTimer()
    {
        while (timeRemaining > 0)
        {
            yield return new WaitForSeconds(1f);
            timeRemaining--;
            UpdateTimerText();
        }

        EndGame();
    }

    private void UpdateTimerText()
    {
        timerText.text = "Time: " + timeRemaining.ToString("F0");
    }

    private void UpdateScoreText()
    {
        scoreText.text = "Score: " + currentScore;
    }

    public void AddScore(int amount)
    {
        currentScore += amount;
        UpdateScoreText();
    }

    private void EndGame()
    {
        gameEnded = true;
        if (currentScore >= scoreToAdvance)
        {
            // Logic to advance to the next level
            Debug.Log("Level Complete! Advancing to the next level.");
            // You can add code here to load the next level
        }
        else
        {
            // Logic for game over
            Debug.Log("Game Over! Try again.");
            // You can add code here to handle game over state
        }
    }

    private IEnumerator SpawnPipes()
    {
        while (!gameEnded)
        {
            SpawnPipe();
            yield return new WaitForSeconds(pipeSpawnInterval);
        }
    }

    private void SpawnPipe()
    {
        GameObject pipe = Instantiate(pipePrefab, new Vector3(10, Random.Range(-1f, 3f), 0), Quaternion.identity);
        pipe.GetComponent<Rigidbody2D>().velocity = Vector2.left * pipeSpeed;
    }

    // This method can be called when the bird passes through pipes
    public void OnPipePassed()
    {
        AddScore(1); // Increase score when passing through pipes
    }

    // This method can be called when the bird collides with a pipe
    public void OnBirdCollision()
    {
        EndGame();
    }

    // This method can be called when the digging tool retrieves an item
    public void OnItemRetrieved(string itemType)
    {
        switch (itemType)
        {
            case "Gold":
                AddScore(10); // Normal score for gold
                break;
            case "Stone":
                AddScore(2); // Reduced score for stone
                break;
            case "NewItem": // New item type
                StartCoroutine(TemporaryScoreBoost(5, 6.0f)); // Boost score by 5 for 6 seconds
                break;
            default:
                break;
        }
    }

    // Coroutine to temporarily boost the score
    private IEnumerator TemporaryScoreBoost(int boostAmount, float duration)
    {
        currentScore += boostAmount;
        UpdateScoreText();
        yield return new WaitForSeconds(duration);
        currentScore -= boostAmount;
        UpdateScoreText();
    }
}