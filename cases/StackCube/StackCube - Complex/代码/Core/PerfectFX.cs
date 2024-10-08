using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class PerfectFX : MonoBehaviour
{
    public static PerfectFX Instance;

    [SerializeField] float _tweenDuration = 1f;
    [SerializeField] TMP_Text _textMesh;
    [SerializeField] Color _defaultColor;
    [SerializeField] Color _fadedColor;

    //private Vector3 _defaultPos;

    private void Awake()
    {
        Instance = this;

        //_defaultPos = transform.position;
    }

    private void OnDestroy()
    {
        Instance = null;
    }

    public void TriggerPerfectText()
    {
        //transform.position = _defaultPos;

        LeanTween.value(gameObject, FadedColor, _defaultColor, _fadedColor, _tweenDuration);
        //LeanTween.moveLocalY(gameObject, _defaultPos.y + .1f, _tweenDuration);
    }

    private void FadedColor(Color val)
    {
        _textMesh.color = val;
    }
}
