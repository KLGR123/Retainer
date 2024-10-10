using UnityEngine;

public class GameControl : MonoBehaviour
{
    // 游戏的时间
    public float gameTime = 60f;

    // Update is called once per frame
    void Update()
    {
        // 游戏时间递减
        gameTime -= Time.deltaTime;
        if (gameTime <= 0)
        {
            // 游戏结束
            EndGame();
        }
    }

    // 游戏结束的处理
    void EndGame()
    {
        // TODO: 游戏结束的处理
    }
}