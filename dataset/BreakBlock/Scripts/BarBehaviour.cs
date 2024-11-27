using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BarBehaviour : MonoBehaviour {

    public float speed = 20f;

    private void Update() {
        if (GameController.state != GameController.GameOverState.playing) {
            gameObject.SetActive(false);
        }
    }

    void FixedUpdate() {
        GetComponent<Rigidbody2D>().velocity = Vector2.right * Input.GetAxisRaw("Horizontal") * speed;
    }
}
