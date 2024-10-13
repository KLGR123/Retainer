using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerControl : MonoBehaviour
{
    public float swingSpeed = 2.0f; // Speed of the swinging motion
    public float hookSpeed = 5.0f; // Speed of the hook when thrown
    public float hookReturnSpeed = 2.0f; // Speed of the hook when returning
    public Transform hook; // Reference to the hook object
    public Transform hookStartPosition; // Starting position of the hook

    private bool isSwinging = false; // Is the hook currently swinging
    private bool isHookThrown = false; // Is the hook currently thrown
    private Vector3 hookTargetPosition; // Target position for the hook

    void Update()
    {
        HandleInput();
        if (isSwinging)
        {
            SwingHook();
        }
        if (isHookThrown)
        {
            MoveHook();
        }
    }

    // Handle player input
    void HandleInput()
    {
        if (Input.GetMouseButtonDown(0))
        {
            if (!isHookThrown)
            {
                isSwinging = !isSwinging; // Toggle swinging state
            }
        }
    }

    // Swing the hook left and right
    void SwingHook()
    {
        float swing = Mathf.Sin(Time.time * swingSpeed) * 2.0f; // Calculate swing position
        hook.position = new Vector3(hookStartPosition.position.x + swing, hookStartPosition.position.y, hookStartPosition.position.z);
    }

    // Move the hook towards the target
    void MoveHook()
    {
        hook.position = Vector3.MoveTowards(hook.position, hookTargetPosition, hookSpeed * Time.deltaTime);
        if (Vector3.Distance(hook.position, hookTargetPosition) < 0.1f)
        {
            // Simulate grabbing an item
            StartCoroutine(ReturnHook());
        }
    }

    // Coroutine to return the hook
    IEnumerator ReturnHook()
    {
        yield return new WaitForSeconds(0.5f); // Simulate grabbing delay
        while (Vector3.Distance(hook.position, hookStartPosition.position) > 0.1f)
        {
            hook.position = Vector3.MoveTowards(hook.position, hookStartPosition.position, hookReturnSpeed * Time.deltaTime);
            yield return null;
        }
        isHookThrown = false;
    }

    // Throw the hook
    public void ThrowHook(Vector3 targetPosition)
    {
        if (!isHookThrown)
        {
            isHookThrown = true;
            isSwinging = false;
            hookTargetPosition = targetPosition;
        }
    }
}