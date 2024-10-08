using UnityEngine;
using UnityEngine.UI;

public class MainMenu : Menu
{
    [Header("UI References :")]
    [SerializeField] Button _creditButton;
    [SerializeField] Button _rateButton;
    [SerializeField] Button _settingsButton;
    [Space]
    [SerializeField] Transform _title;

    public override void SetEnable()
    {
        base.SetEnable();

        _title.localScale = Vector3.one;
        LeanTween.scale(_title.gameObject, Vector3.one * 1.05f, 3f).setEase(LeanTweenType.easeOutQuad).setLoopPingPong();
    }

    public override void SetDisable()
    {
        base.SetDisable();

        _creditButton.interactable = false;
        _settingsButton.interactable = false;
        _rateButton.interactable = false;
    }

    private void Start()
    {
        OnButtonPressed(_creditButton, CreditButtonPressed);
        OnButtonPressed(_rateButton, RateButtonPressed);
        OnButtonPressed(_settingsButton, SettingsButtonPressed);
    }

    private void SettingsButtonPressed()
    {
        MenuManager.Instance.OpenMenu(MenuType.Setting);
    }

    private void RateButtonPressed()
    {
        MenuManager.Instance.OpenMenu(MenuType.Rate);
    }

    private void CreditButtonPressed()
    {
        MenuManager.Instance.OpenMenu(MenuType.Credit);
    }
}
