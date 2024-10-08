using System;
using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class GameoverMenu : Menu
{
    [Header("UI References :")]
    [SerializeField] TMP_Text _scoreText;
    [SerializeField] TMP_Text _bestScoreText;
    [SerializeField] Button _restartButton;
    [SerializeField] Button _homeButton;
    [SerializeField] Button _shareButton;

    //private ShareOnSocialMedia _share;

    protected override void Awake()
    {
        base.Awake();

        //_share = GetComponent<ShareOnSocialMedia>();
    }

    public override void SetEnable()
    {
        base.SetEnable();

        SetScoreDisplay();
    }

    private void Start()
    {
        OnButtonPressed(_restartButton, RestartButton);
        OnButtonPressed(_homeButton, HomeButton);
        OnButtonPressed(_shareButton, HandleShareButton);
    }

    private void HandleShareButton()
    {
        _shareButton.interactable = false;

        //_share.HandleShare();
    }

    private void SetScoreDisplay()
    {
        _scoreText.text = ScoreManager.Instance.Score.ToString();
        _bestScoreText.text = SaveData.GetBestScore().ToString();
    }

    private void HomeButton()
    {
        _restartButton.interactable = false;

        StartCoroutine(ReloadLevelAsync(() =>
        {

            MenuManager.Instance.SwitchMenu(MenuType.Main);
        }));
    }

    private void RestartButton()
    {
        _homeButton.interactable = false;

        StartCoroutine(ReloadLevelAsync(() =>
        {

            MenuManager.Instance.SwitchMenu(MenuType.Gameplay);
        }));
    }

    IEnumerator ReloadLevelAsync(Action OnSceneLoaded = null)
    {
        yield return SceneManager.LoadSceneAsync(SceneManager.GetActiveScene().buildIndex);
        OnSceneLoaded?.Invoke();
    }
}
