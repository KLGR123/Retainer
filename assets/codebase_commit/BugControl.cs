using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BugControl : MonoBehaviour {

    public float minSpeed = 1f;
    public float maxSpeed = 3f;
    public GameObject slowBugPrefab;
    public GameObject fastBugPrefab;
    public GameObject splatEffectPrefab;

    private float speed;

    void Start()
    {
        speed = Random.Range(0f, 1f) < 0.7f ? minSpeed : maxSpeed;
        GameObject bug = speed == minSpeed ? slowBugPrefab : fastBugPrefab;
        Instantiate(bug, transform.position, Quaternion.identity);
    }

    void Update()
    {
        transform.Translate(Vector2.left * speed * Time.deltaTime);
        if (transform.position.x < -10f) // Assuming -10 is out of screen
        {
            Destroy(gameObject);
        }
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Foot"))
        {
            Squash();
        }
    }

    void Squash()
    {
        Instantiate(splatEffectPrefab, transform.position, Quaternion.identity);
        GameControl.instance.BugSquashed(speed == minSpeed ? 1 : 2);
        Destroy(gameObject);
    }
}