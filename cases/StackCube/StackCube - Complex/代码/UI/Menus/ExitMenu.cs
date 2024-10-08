using UnityEngine;
using UnityEngine.UI;

public class ExitMenu : Menu
{
    [Header("UI References :")]
    [SerializeField] Button _yesButton;
    [SerializeField] Button _noButton;

    private void Start()
    {
        OnButtonPressed(_yesButton, YesButtonPressed);
        OnButtonPressed(_noButton, NoButtonPressed);
    }

    public override void SetEnable()
    {
        base.SetEnable();

        _noButton.interactable = true;
        _yesButton.interactable = true;
    }

    private void NoButtonPressed()
    {
        _noButton.interactable = false;

        MenuManager.Instance.CloseMenu();
    }

    private void YesButtonPressed()
    {
        _yesButton.interactable = false;
        Application.Quit();
    }
}
