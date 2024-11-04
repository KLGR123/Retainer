using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SplatEffect : MonoBehaviour
{
    public Sprite splatSprite;

    public void ShowSplatEffect(Vector3 position)
    {
        GameObject splat = new GameObject("Splat");
        SpriteRenderer renderer = splat.AddComponent<SpriteRenderer>();
        renderer.sprite = splatSprite;
        splat.transform.position = position;
        StartCoroutine(RemoveSplatAfterTime(splat, 0.5f));
    }

    private IEnumerator RemoveSplatAfterTime(GameObject splat, float time)
    {
        yield return new WaitForSeconds(time);
        Destroy(splat);
    }
}