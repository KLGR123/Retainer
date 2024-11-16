using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoleControl : MonoBehaviour {

    public float appearDuration = 1.0f; // Time the mole stays visible
    public float riseSpeed = 2.0f; // Speed at which the mole rises
    public float fallSpeed = 2.0f; // Speed at which the mole falls
    private bool isVisible = false;
    private Animator animator;
    private Vector3 initialPosition;
    private Vector3 targetPosition;

    void Start()
    {
        animator = GetComponent<Animator>();
        initialPosition = transform.position;
        targetPosition = new Vector3(initialPosition.x, initialPosition.y + 1.0f, initialPosition.z); // Adjust the target position as needed
        StartCoroutine(MoleBehavior());
    }

    IEnumerator MoleBehavior()
    {
        while (true)
        {
            yield return new WaitForSeconds(Random.Range(0.5f, 2.0f)); // Random delay before appearing
            StartCoroutine(Rise());
            yield return new WaitForSeconds(appearDuration);
            if (isVisible) // If not hit, start falling
            {
                StartCoroutine(Fall());
            }
        }
    }

    IEnumerator Rise()
    {
        isVisible = true;
        animator.SetTrigger("Appear");
        while (transform.position.y < targetPosition.y)
        {
            transform.position = Vector3.MoveTowards(transform.position, targetPosition, riseSpeed * Time.deltaTime);
            yield return null;
        }
    }

    IEnumerator Fall()
    {
        isVisible = false;
        animator.SetTrigger("Disappear");
        while (transform.position.y > initialPosition.y)
        {
            transform.position = Vector3.MoveTowards(transform.position, initialPosition, fallSpeed * Time.deltaTime);
            yield return null;
        }
    }

    void OnMouseDown()
    {
        if (isVisible)
        {
            GameControl.instance.MoleHit();
            StopAllCoroutines();
            StartCoroutine(Fall());
        }
    }
}