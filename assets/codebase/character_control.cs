using UnityEngine;

public class CharacterControl : MonoBehaviour {
    public float speed = 10.0f;

    void Update() {
        float moveHorizontal = Input.GetAxis('Horizontal');
        float moveVertical = Input.GetAxis('Vertical');

        Vector3 movement = new Vector3(moveHorizontal, 0.0f, moveVertical);

        GetComponent<Rigidbody>().AddForce(movement * speed);
    }
}