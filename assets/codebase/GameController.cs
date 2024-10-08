using System.Collections;

  using System.Collections.Generic;

  using UnityEngine;


  public class GameController : MonoBehaviour {

    // 游戏是否结束

    private bool isGameOver = false;


    // 游戏主循环

    void Update() {

      if (isGameOver) {

        return;

      }

      // TODO: 方块的生成和移动

    }


    // 游戏结束的判断

    public void GameOver() {

      isGameOver = true;

    }

  }