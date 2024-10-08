using UnityEngine;

public class OtherCharacterControl : MonoBehaviour {
    public float speed = 10.0f;

    void Update() {
        float moveHorizontal = Random.Range(-1.0f, 1.0f);
        float moveVertical = Random.Range(-1.0f, 1.0f);

        Vector3 movement = new Vector3(moveHorizontal, 0.0f, moveVertical);

        GetComponent<Rigidbody>().AddForce(movement * speed);
    }
}