using UnityEngine;
using UnityEngine.UI;

public class UIControl : MonoBehaviour
{
    // 得分显示的文本
    public Text scoreText;

    // 更新得分显示
    public void UpdateScore(int score)
    {
        scoreText.text = "Score: " + score;
    }
}