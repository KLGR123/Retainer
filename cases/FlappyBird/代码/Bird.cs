using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bird : MonoBehaviour
{
    public float upForce = 200f;
    public int player_num;

    private bool isDead = false;
    private bool isDead2 = false;
    private Rigidbody2D rb2d;
    private Animator anim;
    
    // Use this for initialization
    void Start()
    {
        rb2d = GetComponent<Rigidbody2D> ();
        anim = GetComponent<Animator> ();
    }
    
    // Update is called once per frame
    void Update()
    {
        if (isDead == false)
        {
            if (Input.GetMouseButtonDown(0) && player_num == 0) //left click
            {
                rb2d.velocity = Vector2.zero;
                rb2d.AddForce(new Vector2 (0, upForce));
                anim.SetTrigger("Flap");
            }
        }
        if (isDead2 == false)
        {
            if (Input.GetKeyDown(KeyCode.Space) && player_num == 1)
            {
                rb2d.velocity = Vector2.zero;
                rb2d.AddForce(new Vector2(0, upForce));
                anim.SetTrigger("Flap");
            }
        }
    }

    void OnCollisionEnter2D()
    {
        // Debug.Log("Player #: " + player_num);
        // Debug.Log("players: " + num_players);

        if (isDead == false && player_num == 0)
        {
            rb2d.velocity = Vector2.zero;
            isDead = true;
            anim.SetTrigger("Die");
            GameControl.instance.BirdDied();
        }

    }

}

