using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Stacks : MonoBehaviour
{
    int stack_long;
    int count = 4;
    const float max_value = 5f;
    const float speed_value = 0.02f;
    const float size = 3f;
    Vector2 stac_size = new Vector2(size, size);
    float tolarance=0.1f;
    float speed = speed_value;
    GameObject[] Go_stack;
    int stack_index;
    bool x_movement;
    Vector3 cam_pos;
    Vector3 osp; //old stack pos 
    float sens; //sensitivity
    bool stack_take;
    bool dead = false;
    int combo = 0;
    Color32 col;
    public Color32 col1;
    public Color32 col2;
    public Color32 col3;
    public Color32 col4;
    int counter = 0;
    Camera camera;

    void Start()
    {
        camera = GameObject.FindGameObjectWithTag("MainCamera").GetComponent<Camera>();
        camera.backgroundColor = col2;
        col = col1;
        stack_long = transform.GetChildCount();
        Go_stack = new GameObject[stack_long];
        for (int i = 0; i < stack_long; i++)
        {
            Go_stack[i] = transform.GetChild(i).gameObject;
            Go_stack[i] . GetComponent<Renderer>().material.color = col;
        }
        stack_index = stack_long - 1;
    }
    void leftover_piece(Vector3 loc, Vector3 scale )
    {
        GameObject go = GameObject.CreatePrimitive(PrimitiveType.Cube);
        go.transform.localScale = scale;
        go.transform.position = loc;
        go.GetComponent<Renderer>().material.color = Color32.Lerp(go.GetComponent<Renderer>().material.color, col, 0.5f);
        go.AddComponent<Rigidbody>();
    }


    void Update()
    {
        if (!dead)
        {
            if (Input.GetMouseButtonDown(0))
            {
                if (stack_controll())
                {
                    Stack_Take_Put();
                    count++;
                    byte val = 25;
                    col = new Color32((byte)(col.r + val), (byte)(col.g + val), (byte)(col.b + val),col.a);
                    col2 = new Color32((byte)(col2.r + val), (byte)(col2.g + val), (byte)(col2.b + val), col2.a);
                    if (counter>3)
                    {
                        counter = 0;
                        col1 = col2;
                        col2 = col3;
                        col3 = col4;
                        col4 = col;
                        col = col1;
                    }
                    counter++;
                }
                else
                {
                    finish();
                }

            }
            movement();
            transform.position = Vector3.Lerp(transform.position, cam_pos, 0.1f);
        }
    }
    void Stack_Take_Put()
    {
        osp = Go_stack[stack_index].transform.localPosition;
        if (stack_index <= 0)
        {
            stack_index = stack_long;
        }
        stack_take = false;
        stack_index--;
        x_movement = !x_movement;
        cam_pos = new Vector3(0, -count+3, 0);
        Go_stack[stack_index].transform.localScale = new Vector3(stac_size.x, 1, stac_size.y);
        Go_stack[stack_index].GetComponent<Renderer>().material.color = Color32.Lerp(Go_stack[stack_index].GetComponent<Renderer>().material.color,col,0.5f);
        camera.backgroundColor = Color32.Lerp(camera.backgroundColor, col2, 0.2f);

    }
    void movement()
    {
        if (x_movement)
        {
            if (!stack_take)
            {
                Go_stack[stack_index].transform.localPosition = new Vector3(-4, count, sens);
                stack_take = true;
            }
            if (Go_stack[stack_index].transform.localPosition.x > max_value)
            {
                speed = speed_value * -1;
            }
            else if (Go_stack[stack_index].transform.localPosition.x < -max_value)
            {
                speed = speed_value;
            }
            Go_stack[stack_index].transform.localPosition += new Vector3(speed, 0, 0);
        }
        else
        {
            if (!stack_take)
            {
                Go_stack[stack_index].transform.localPosition = new Vector3(sens, count, -4);
                stack_take = true;
            }
            if (Go_stack[stack_index].transform.localPosition.z > max_value)
            {
                speed = speed_value * -1;
            }
            else if (Go_stack[stack_index].transform.localPosition.z < -max_value)
            {
                speed = speed_value;
            }
            Go_stack[stack_index].transform.localPosition += new Vector3(0, 0, speed);
        }
    }
    bool stack_controll()
    {
        if (x_movement)
        {
            float diff = osp.x - Go_stack[stack_index].transform.localPosition.x;
            if (Mathf.Abs(diff) > tolarance)
            {
                combo = 0;
                Vector3 local;
                if (Go_stack[stack_index].transform.localPosition.x > osp.x)
                {
                    local = new Vector3(Go_stack[stack_index].transform.position.x + Go_stack[stack_index].transform.localScale.x / 2, Go_stack[stack_index].transform.position.y, Go_stack[stack_index].transform.position.z);
                }
                else
                {
                    local = new Vector3(Go_stack[stack_index].transform.position.x - Go_stack[stack_index].transform.localScale.x / 2, Go_stack[stack_index].transform.position.y, Go_stack[stack_index].transform.position.z);

                }
                Vector3 sizee = new Vector3(diff, 1, stac_size.y);
                stac_size.x -= Mathf.Abs(diff);
                if (stac_size.x < 0)
                {
                    return false;
                }
                Go_stack[stack_index].transform.localScale = new Vector3(stac_size.x, 1, stac_size.y);
                float mid = Go_stack[stack_index].transform.localPosition.x / 2 + osp.x / 2;
                Go_stack[stack_index].transform.localPosition = new Vector3(mid, count, osp.z);
                sens = Go_stack[stack_index].transform.localPosition.x;
                leftover_piece(local, sizee);
            }
            else
            {
                combo++;
                if (combo >3)
                {
                    stac_size.x += 0.3f;
                    if (stac_size.x>size)
                    {
                        stac_size.x = size;
                        Go_stack[stack_index].transform.localScale = new Vector3(stac_size.x, 1, stac_size.y);
                        float mid = Go_stack[stack_index].transform.localPosition.x / 2 + osp.x / 2;
                        Go_stack[stack_index].transform.localPosition = new Vector3(mid, count, osp.z);
                     
                    }
                }
                else
                {
                    Go_stack[stack_index].transform.localPosition = new Vector3(osp.x, count, osp.z);

                }
                sens = Go_stack[stack_index].transform.localPosition.x;
            }
        }
        else
        {
            float diff = osp.z - Go_stack[stack_index].transform.localPosition.z;
            if (Mathf.Abs(diff) > tolarance)
            {
                combo = 0;
                Vector3 local;
                if (Go_stack[stack_index].transform.localPosition.z > osp.z)
                {
                    local = new Vector3(Go_stack[stack_index].transform.position.x, Go_stack[stack_index].transform.position.y, Go_stack[stack_index].transform.position.z + Go_stack[stack_index].transform.localScale.z / 2);
                }
                else
                {
                    local = new Vector3(Go_stack[stack_index].transform.position.x, Go_stack[stack_index].transform.position.y, Go_stack[stack_index].transform.position.z - Go_stack[stack_index].transform.localScale.z / 2);

                }
                Vector3 sizee = new Vector3(stac_size.x, 1, diff);
                stac_size.y -= Mathf.Abs(diff);
                if (stac_size.y < 0)
                {
                    return false;
                }
                Go_stack[stack_index].transform.localScale = new Vector3(stac_size.x, 1, stac_size.y);
                float mid = Go_stack[stack_index].transform.localPosition.z / 2 + osp.z / 2;
                Go_stack[stack_index].transform.localPosition = new Vector3(osp.x, count, mid);
                sens = Go_stack[stack_index].transform.localPosition.z;
                leftover_piece(local, sizee);
                combo++;
            }
            else
            {
                combo++;
                if (combo > 3)
                {
                    stac_size.y += 0.3f;
                    if (stac_size.x > size)
                    {
                        stac_size.y = size;
                        Go_stack[stack_index].transform.localScale = new Vector3(stac_size.x, 1, stac_size.y);
                        float mid = Go_stack[stack_index].transform.localPosition.z / 2 + osp.z / 2;
                        Go_stack[stack_index].transform.localPosition = new Vector3(osp.x, count, mid);
                    }
                }
                else
                {
                    Go_stack[stack_index].transform.localPosition = new Vector3(osp.x, count, osp.z);

                }
                sens = Go_stack[stack_index].transform.localPosition.z;

            }

        }
        return true;
    }
    void finish()
    {
        dead = true;
        Go_stack[stack_index].AddComponent<Rigidbody>(); 
    } 
}
 