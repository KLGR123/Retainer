using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BugControl : MonoBehaviour {

    public float speed;
    public int points;
    private bool isSquashed = false;

    void Start()
    {
        // Randomly set speed and points based on bug type
        if (gameObject.CompareTag("FastBug"))
        {
            speed = Random.Range(3f, 5f);
            points = 2;
        }
        else if (gameObject.CompareTag("SlowBug"))
        {
            speed = Random.Range(1f, 2f);
            points = 1;
        }
    }

    void Update()
    {
        if (!isSquashed)
        {
            transform.Translate(Vector2.left * speed * Time.deltaTime);
        }
    }

    public void Squash()
    {
        if (!isSquashed)
        {
            isSquashed = true;
            GameControl.instance.BugSquashed(points);
            StartCoroutine(ShowSplatEffect());
        }
    }

    private IEnumerator ShowSplatEffect()
    {
        // Show splat effect
        GameObject splat = Instantiate(Resources.Load("Splat") as GameObject, transform.position, Quaternion.identity);
        yield return new WaitForSeconds(0.5f);
        Destroy(splat);
        Destroy(gameObject);
    }

    private void OnBecameInvisible()
    {
        if (!isSquashed)
        {
            GameControl.instance.ResetCombo();
            Destroy(gameObject);
        }
    }
}