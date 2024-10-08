using System;
using UnityEngine;
using UnityEngine.UI;

public enum AnimationTypes
{
    Fade,
    Move,
    Scale
}

public class TweenUI : MonoBehaviour
{
    [System.Serializable]
    private class TweenStat
    {
        public float _duration = .2f;
        public float _delay = 0;

        public Vector3 _from;
        public Vector3 _to;

        public AnimationTypes _animationType;
        public LeanTweenType _easeType;

        public LTDescr _tweenObj;
    }

    [SerializeField] bool _ignoreTimeScale = false;
    [SerializeField] TweenStat _onEnable;
    [SerializeField] TweenStat _onDisable;

    private CanvasGroup _cg;

    private RectTransform _rect;
    private Vector3 _defaultPos;
    private Button _button;

    private void Awake()
    {
        _rect = GetComponent<RectTransform>();
        _button = GetComponent<Button>();
        _defaultPos = _rect.anchoredPosition;
    }

    public void HandleOnEnable()
    {
        ResetTweenValue();

        if (_button) _button.interactable = false;
        HandleTween(_onEnable, EnableButton);
    }

    public void HandleOnDisable()
    {
        if (_button) _button.interactable = false;
        HandleTween(_onDisable);
    }

    public float GetOnDisableDuration()
    {
        return _onDisable._delay + _onDisable._duration;
    }

    private void EnableButton()
    {
        if (_button) _button.interactable = true;
    }

    private void HandleTween(TweenStat stat, Action onComplete = null)
    {
        LeanTween.cancel(this.gameObject);

        switch (stat._animationType)
        {
            case AnimationTypes.Fade:
                Fade(stat);
                break;
            case AnimationTypes.Move:
                Move(stat);
                break;
            case AnimationTypes.Scale:
                Scale(stat);
                break;
        }

        stat._tweenObj.setEase(stat._easeType).setDelay(stat._delay);

        if (onComplete != null)
        {
            stat._tweenObj.setOnComplete(onComplete);
        }

        if (_ignoreTimeScale)
        {
            stat._tweenObj.setIgnoreTimeScale(true);
        }
    }

    private void Move(TweenStat stat)
    {
        _rect.anchoredPosition = _defaultPos + stat._from;

        stat._tweenObj = LeanTween.move(_rect, _defaultPos + stat._to, stat._duration);
    }

    private void Scale(TweenStat stat)
    {
        _rect.localScale = stat._from;

        stat._tweenObj = LeanTween.scale(_rect, stat._to, stat._duration);
    }

    private void Fade(TweenStat stat)
    {
        _cg = gameObject.GetComponent<CanvasGroup>();
        if (!_cg) _cg = gameObject.AddComponent<CanvasGroup>();

        _cg.alpha = stat._from.x;

        stat._tweenObj = LeanTween.alphaCanvas(_cg, stat._to.x, stat._duration);
    }

    private void ResetTweenValue()
    {
        if (_cg) _cg.alpha = 1f;
        if (_rect) _rect.anchoredPosition = _defaultPos;
        if (_rect) _rect.localScale = Vector3.one;
    }
}