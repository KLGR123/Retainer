using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SplatEffect : MonoBehaviour {

    public float duration = 0.5f; // Duration for which the splat effect is visible

    void Start()
    {
        Destroy(gameObject, duration);
    }
}