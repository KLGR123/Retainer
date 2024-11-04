using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FootControl : MonoBehaviour
{
    public float stompSpeed = 5f;
    public Sprite normalFootSprite;
    public Sprite bigFootSprite;
    private SpriteRenderer spriteRenderer;
    private bool isStomping = false;
    private bool hasBigFootBuff = false;

    void Start()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            StartCoroutine(Stomp());
        }
    }

    private IEnumerator Stomp()
    {
        if (!isStomping)
        {
            isStomping = true;
            Vector3 originalPosition = transform.position;
            Vector3 targetPosition = new Vector3(transform.position.x, transform.position.y - 1, transform.position.z);

            while (transform.position.y > targetPosition.y)
            {
                transform.position = Vector3.MoveTowards(transform.position, targetPosition, stompSpeed * Time.deltaTime);
                yield return null;
            }

            // Check for bugs under the foot
            Collider2D[] hitColliders = Physics2D.OverlapCircleAll(transform.position, hasBigFootBuff ? 1.5f : 1f);
            foreach (var hitCollider in hitColliders)
            {
                if (hitCollider.CompareTag("Bug"))
                {
                    hitCollider.GetComponent<BugControl>().Squash();
                }
            }

            while (transform.position.y < originalPosition.y)
            {
                transform.position = Vector3.MoveTowards(transform.position, originalPosition, stompSpeed * Time.deltaTime);
                yield return null;
            }

            isStomping = false;
        }
    }

    public void ActivateBigFootBuff()
    {
        hasBigFootBuff = true;
        spriteRenderer.sprite = bigFootSprite;
        StartCoroutine(DeactivateBigFootBuffAfterTime(10f));
    }

    private IEnumerator DeactivateBigFootBuffAfterTime(float time)
    {
        yield return new WaitForSeconds(time);
        hasBigFootBuff = false;
        spriteRenderer.sprite = normalFootSprite;
    }
}