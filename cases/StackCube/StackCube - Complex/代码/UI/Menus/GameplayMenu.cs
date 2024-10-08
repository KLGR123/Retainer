using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class GameplayMenu : Menu
{
    [Header("UI References :")]
    [SerializeField] private TMP_Text _scoreText;
    [SerializeField] Button _pauseButton;

    public override void SetEnable()
    {
        base.SetEnable();
        //_pauseButton.interactable = true;

        UpdateScore();
    }

    private void Start()
    {
        OnButtonPressed(_pauseButton, PauseButtonPressed);
    }

    private void UpdateScore()
    {
        int score = ScoreManager.Instance.Score;
        _scoreText.text = score.ToString();
    }

    private void PauseButtonPressed()
    {
        //_pauseButton.interactable = false;

        Time.timeScale = 0f;
        MenuManager.Instance.OpenMenu(MenuType.Pause);
    }

    private void OnEnable()
    {
        ScoreManager.OnScoreUpdated += UpdateScore;
    }

    private void OnDisable()
    {
        ScoreManager.OnScoreUpdated -= UpdateScore;
    }
}