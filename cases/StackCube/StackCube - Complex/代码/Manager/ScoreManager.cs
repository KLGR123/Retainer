using System;
using UnityEngine;

public class ScoreManager : MonoBehaviour
{
    public static ScoreManager Instance;

    public static event Action OnScoreUpdated;

    public static event Action<int> OnGameFinished;

    private int _score;
    private int _scoreMultiplier = 1;

    public int Score => _score;

    private void OnEnable()
    {
        Instance = this;
        MovingCube.OnCubeStack += MovingCube_OnCubeStack;
        GameManager.OnGameEnd += GameManager_OnGameEnd;
    }

    private void MovingCube_OnCubeStack(bool isPerfect)
    {
        if (isPerfect)
        {
            _scoreMultiplier++;

            SoundManager.Instance.PlayAudio(AudioType.PERFECT);
            VibrationManager.Instance.StartVibration();
        }
        else
        {
            _scoreMultiplier = 1;
        }

        _score += Mathf.Clamp(_scoreMultiplier,1,6);

        OnScoreUpdated?.Invoke();

        SoundManager.Instance.PlayAudio(AudioType.DROP);
    }

    private void OnDisable()
    {
        Instance = null;
        MovingCube.OnCubeStack -= MovingCube_OnCubeStack;
        GameManager.OnGameEnd -= GameManager_OnGameEnd;
    }

    private void GameManager_OnGameEnd()
    {
        UpdateBestScore();
    }

    private void UpdateBestScore()
    {
        int bestScore;

        bestScore = SaveData.GetBestScore();
        if (_score > bestScore)
        {
            OnGameFinished.Invoke(_score);
            SaveData.SetBestScore(_score);
        }
    }
}