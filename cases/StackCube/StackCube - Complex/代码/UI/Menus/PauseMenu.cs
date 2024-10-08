using UnityEngine;
using UnityEngine.UI;

public class PauseMenu : Menu
{
    [Header("UI References :")]
    [SerializeField] Button _resumeButton;
    [SerializeField] private Button _toggleMusicButton;
    [SerializeField] private Button _toggleSFXButton;
    [SerializeField] private Button _toggleVibrateButton;

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
        _resumeButton.interactable = true;

        SetIconToggle();
    }

    private void Start()
    {
        _musicImage = _toggleMusicButton.GetComponent<Image>();
        _sfxImage = _toggleSFXButton.GetComponent<Image>();
        _vibrateImage = _toggleVibrateButton.GetComponent<Image>();

        OnButtonPressed(_resumeButton, ResumeButtonPressed);

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

    private void ResumeButtonPressed()
    {
        Time.timeScale = 1f;

        _resumeButton.interactable = false;

        MenuManager.Instance.CloseMenu();
    }
}