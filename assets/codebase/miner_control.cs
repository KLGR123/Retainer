using UnityEngine;

public class MinerControl : MonoBehaviour
{
    // 矿工的移动速度
    public float speed = 10f;

    // Update is called once per frame
    void Update()
    {
        // 控制矿工的移动
        float moveHorizontal = Input.GetAxis('Horizontal');
        Vector3 movement = new Vector3(moveHorizontal, 0.0f, 0.0f);
        transform.position = transform.position + movement * speed * Time.deltaTime;
    }
}