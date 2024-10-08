using System;
using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class SettingMenu : Menu
{
    [Header("Inherit References :")]
    [SerializeField] private Button _adsButton;
    [SerializeField] private Button _policyButton;
    [SerializeField] private Button _closeButton;
    [SerializeField] private Button _toggleMusicButton;
    [SerializeField] private Button _toggleSFXButton;
    [SerializeField] private Button _toggleVibrateButton;

    [Space]
    [SerializeField] private RectTransform _panel;

    [Header("SFX Image Toggle")]
    [SerializeField] Sprite _sfxTrue;
    [SerializeField] Sprite _sfxFalse;

    [Header("Music Image Toggle")]
    [SerializeField] Sprite _musicTrue;
    [SerializeField] Sprite _musicFalse;

    [Header("Vibrate Image Toggle")]
    [SerializeField] Sprite _vibrateTrue;
    [SerializeField] Sprite _vibrateFalse;

    private Image _musicImage;
    private Image _sfxImage;
    private Image _vibrateImage;

    public override void SetEnable()
    {
        base.SetEnable();
        _adsButton.interactable = true;
        _policyButton.interactable = true;
        _closeButton.interactable = true;

        SetIconToggle();
    }

    private void Start()
    {
       /* bool isUsingAdmob = AdsManager.Instance.adsType == AdsType.Admob;*/
       /* _adsButton.gameObject.SetActive(isUsingAdmob);
        _policyButton.gameObject.SetActive(isUsingAdmob);*/
       /* if (isUsingAdmob) _panel.sizeDelta = new Vector2(600, 560);
        else */_panel.sizeDelta = new Vector2(600, 300);

        _musicImage = _toggleMusicButton.GetComponent<Image>();
        _sfxImage = _toggleSFXButton.GetComponent<Image>();
        _vibrateImage = _toggleVibrateButton.GetComponent<Image>();

        OnButtonPressed(_adsButton, AdsButtonListener);
        OnButtonPressed(_policyButton, PolicyButtonListener);
        OnButtonPressed(_closeButton, CloseButtonListener);
        OnButtonPressed(_toggleMusicButton, ToggleMusicButtonListener);
        OnButtonPressed(_toggleSFXButton, ToggleSFXButtonListener);
        OnButtonPressed(_toggleVibrateButton, ToggleVibrateButtonListener);

        SetIconToggle();
    }

    private void SetIconToggle()
    {
        _musicImage.sprite = SaveData.GetMusicState() ? _musicTrue : _musicFalse;
        _sfxImage.sprite = SaveData.GetSfxState() ? _sfxTrue : _sfxFalse;
        _vibrateImage.sprite = SaveData.GetVibrateState() ? _vibrateTrue : _vibrateFalse;
    }

    private void ToggleMusicButtonListener()
    {
        SoundManager.Instance.ToggleMusic();
        _musicImage.sprite = SaveData.GetMusicState() ? _musicTrue : _musicFalse;
    }

    private void ToggleSFXButtonListener()
    {
        SoundManager.Instance.ToggleFX();
        _sfxImage.sprite = SaveData.GetSfxState() ? _sfxTrue : _sfxFalse;
    }

    private void ToggleVibrateButtonListener()
    {
        VibrationManager.Instance.ToggleVibration();
        _vibrateImage.sprite = SaveData.GetVibrateState() ? _vibrateTrue : _vibrateFalse;

        VibrationManager.Instance.StartVibration();
    }

    private void CloseButtonListener()
    {
        _closeButton.interactable = false;
        MenuManager.Instance.CloseMenu();
    }

    private void AdsButtonListener()
    {
        _adsButton.interactable = false;

        PlayerPrefs.SetInt("npa", -1);

        SoundManager.Instance.DestroyObject();

        //load gdpr scene
        StartCoroutine(LoadGDPRAsyncScene());
    }

    IEnumerator LoadGDPRAsyncScene()
    {
        yield return SceneManager.LoadSceneAsync(0);
        MenuManager.Instance.DestroyObject();
    }

    private void PolicyButtonListener()
    {

    }
}
