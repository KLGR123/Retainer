using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BugControl : MonoBehaviour
{
    public float minSpeed = 1f;
    public float maxSpeed = 3f;
    public bool isFastBug = false;
    private float speed;
    private bool isSquashed = false;

    void Start()
    {
        speed = isFastBug ? maxSpeed : minSpeed;
    }

    void Update()
    {
        if (!isSquashed)
        {
            transform.Translate(Vector3.left * speed * Time.deltaTime);
            if (transform.position.x < -10f) // If bug goes off screen
            {
                GameControl.instance.MissedBug();
                Destroy(gameObject);
            }
        }
    }

    public void Squash()
    {
        if (!isSquashed)
        {
            isSquashed = true;
            GameControl.instance.BugSquashed(isFastBug);
            StartCoroutine(SplatEffect());
        }
    }

    private IEnumerator SplatEffect()
    {
        // Show splat effect
        GetComponent<SpriteRenderer>().sprite = Resources.Load<Sprite>("BugSplat");
        yield return new WaitForSeconds(0.5f);
        Destroy(gameObject);
    }
}