using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Column : MonoBehaviour {

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.GetComponent<Bird> () != null)
        {

            // GameControl.instance.Bird2Scored();
            if (other.CompareTag("B1"))
            {
                GameControl.instance.BirdScored();
            }

        }
    }
}
