using UnityEngine;

public class GameControl : MonoBehaviour {
    public GameObject character;

    void Update() {
        if(character.transform.position.y < -20) {
            Debug.Log("Game Over!");
        }
    }
}