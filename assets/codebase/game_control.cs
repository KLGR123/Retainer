using UnityEngine;

public class GameControl : MonoBehaviour {
    public GameObject character;

    void Update() {
        if(character.transform.position.y < -10) {
            Debug.Log("Game Over!");
        }
    }
}