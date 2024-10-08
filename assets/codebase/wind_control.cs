using UnityEngine;

public class WindControl : MonoBehaviour {
    public float force = 10.0f;

    void Update() {
        Vector3 windForce = new Vector3(force, 0.0f, 0.0f);
        GetComponent<Rigidbody>().AddForce(windForce);
    }
}