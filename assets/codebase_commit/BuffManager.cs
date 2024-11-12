using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BuffManager : MonoBehaviour {

    public FootControl footControl;
    public float bigFootDuration = 10f;
    private int consecutiveSquashes = 0;
    private const int squashesForBuff = 10;

    public void BugSquashed()
    {
        consecutiveSquashes++;
        if (consecutiveSquashes >= squashesForBuff)
        {
            ActivateBigFootBuff();
            consecutiveSquashes = 0;
        }
    }

    private void ActivateBigFootBuff()
    {
        footControl.ActivateBigFoot(bigFootDuration);
    }
}