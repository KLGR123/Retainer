using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BuffControl : MonoBehaviour
{
    private FootControl footControl;

    void Start()
    {
        footControl = GetComponent<FootControl>();
    }

    public void ActivateBigFootBuff()
    {
        footControl.ActivateBigFootBuff();
    }
}