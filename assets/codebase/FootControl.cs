using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FootControl : MonoBehaviour {

    public static FootControl instance;
    public float stompSpeed = 5f;
    public Sprite normalFootSprite;
    public Sprite bigFootSprite;
    private Vector2 originalPosition;
    private bool isStomping = false;
    private SpriteRenderer spriteRenderer;

    void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else if (instance != this)
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        originalPosition = transform.position;
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0) && !isStomping)
        {
            StartCoroutine(Stomp());
        }
    }

    private IEnumerator Stomp()
    {
        isStomping = true;
        Vector2 targetPosition = new Vector2(transform.position.x, transform.position.y - 1f);

        while (Vector2.Distance(transform.position, targetPosition) > 0.01f)
        {
            transform.position = Vector2.MoveTowards(transform.position, targetPosition, stompSpeed * Time.deltaTime);
            yield return null;
        }

        yield return new WaitForSeconds(0.1f);

        while (Vector2.Distance(transform.position, originalPosition) > 0.01f)
        {
            transform.position = Vector2.MoveTowards(transform.position, originalPosition, stompSpeed * Time.deltaTime);
            yield return null;
        }

        isStomping = false;
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        BugControl bug = other.GetComponent<BugControl>();
        if (bug != null)
        {
            bug.Squash();
        }
    }

    public void ActivateBigFoot()
    {
        spriteRenderer.sprite = bigFootSprite;
        // Optionally increase the collider size
    }

    public void DeactivateBigFoot()
    {
        spriteRenderer.sprite = normalFootSprite;
        // Optionally reset the collider size
    }
}