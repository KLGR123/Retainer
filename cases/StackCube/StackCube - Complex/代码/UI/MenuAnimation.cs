using System;
using System.Collections;
using UnityEngine;

public class MenuAnimation : MonoBehaviour
{
    [SerializeField] protected TweenUI[] _objectToAnimate;

    Coroutine disableRoutine;

    public void PlayTweenEnable()
    {
        if (disableRoutine != null)
            StopCoroutine(disableRoutine);

        foreach (var obj in _objectToAnimate)
        {
            obj.HandleOnEnable();
        }
    }

    public void PlayTweenDisable(Action onComplete)
    {
        float tweenDuration = 0f;

        foreach (var obj in _objectToAnimate)
        {
            obj.HandleOnDisable();

            // get the longest onDisable tween duration
            float duration = obj.GetOnDisableDuration();
            if (tweenDuration < duration)
                tweenDuration = duration;
        }

        disableRoutine = StartCoroutine(DisableGameobjectRoutine(onComplete, tweenDuration));
    }

    protected IEnumerator DisableGameobjectRoutine(Action onComplete, float duration)
    {
        yield return new WaitForSeconds(duration);
        onComplete?.Invoke();
    }
}