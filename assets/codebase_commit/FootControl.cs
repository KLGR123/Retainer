using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FootControl : MonoBehaviour {

    public GameObject bigFootPrefab;
    public float stompCooldown = 0.5f;
    private float lastStompTime;
    private bool isBigFootActive = false;

    void Update()
    {
        if (Input.GetMouseButtonDown(0) && Time.time > lastStompTime + stompCooldown)
        {
            Stomp();
            lastStompTime = Time.time;
        }
    }

    void Stomp()
    {
        Vector3 stompPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        stompPosition.z = 0;
        if (isBigFootActive)
        {
            Instantiate(bigFootPrefab, stompPosition, Quaternion.identity);
        }
        else
        {
            transform.position = stompPosition;
            // Logic to check for bugs under the foot and squash them
        }
    }

    public void ActivateBigFoot(float duration)
    {
        StartCoroutine(BigFootRoutine(duration));
    }

    private IEnumerator BigFootRoutine(float duration)
    {
        isBigFootActive = true;
        yield return new WaitForSeconds(duration);
        isBigFootActive = false;
    }
}