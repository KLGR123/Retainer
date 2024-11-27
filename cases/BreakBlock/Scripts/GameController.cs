using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameController : MonoBehaviour {

    public Transform brick;
    public Text textPoints;
    public Text textResult;
    public enum GameOverState { playing, win, lose};
    public static GameOverState state = GameOverState.playing;

    private static int points;
    private int rPoints;

    public static int Points {
        get => points;
        set {
            if (points <= 0) {
                state = GameOverState.win;
            }
            points = value;
        }
    }

    private void Awake() {
        CreateBricks();
    }

    void Start() {
        rPoints = points;
    }

    private void Update() {
        textPoints.text = "Points: " + (rPoints - points);
        if (state.Equals(GameOverState.win)) {
            GameOver(true);
        }
        if (state.Equals(GameOverState.lose)) {
            GameOver(false);
        }
    }

    /// <summary>
    /// Finish the game
    /// True if win or false if lose.
    /// </summary>
    public void GameOver(bool win) {
        if (win) {
            textResult.text = "YOU WIN!";
        } else {
            textResult.text = "YOU LOSE!";
        }
        textResult.gameObject.SetActive(true);
    }

    public void CreateBricks() {
        for (float y = 2; y > 0; y = y - 1.179f) {
            for (float x = -9; x < 9; x = x + 1.196f) {
                Instantiate(brick, new Vector3(x, y, 0), Quaternion.identity);
                points++;
            }
        }
    }
    
}
