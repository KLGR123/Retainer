using System.Collections;

  using System.Collections.Generic;

  using UnityEngine;

  using UnityEngine.UI;


  public class UIController : MonoBehaviour {

    // 游戏得分

    public Text scoreText;


    // 更新得分

    public void UpdateScore(int score) {

      scoreText.text = "Score: " + score;

    }

  }