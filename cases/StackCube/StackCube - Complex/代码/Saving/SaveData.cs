using System;
using UnityEngine;

public static class SaveData
{
    // Static Constructor
    // use it to load once when the game is running. 
    // (it will execute only once, even when scene is changed)
    static SaveData()
    {
        // Load data
    }

    public static int GetBestScore()
    {
        return PlayerPrefs.GetInt("BestScore", 0);
    }

    public static void SetBestScore(int score)
    {
        PlayerPrefs.SetInt("BestScore", score);
    }

    public static bool GetMusicState()
    {
        return PlayerPrefs.GetInt("MusicState", 0) == 0;
    }

    public static void SetMusicState(bool val)
    {
        int intVal = val ? 0 : 1;
        PlayerPrefs.SetInt("MusicState", intVal);
    }

    public static bool GetSfxState()
    {
        return PlayerPrefs.GetInt("SfxState", 0) == 0;
    }

    public static void SetSfxState(bool val)
    {
        int intVal = val ? 0 : 1;
        PlayerPrefs.SetInt("SfxState", intVal);
    }

    public static bool GetVibrateState()
    {
        return PlayerPrefs.GetInt("VibrateState", 0) == 0;
    }

    public static void SetVibrateState(bool val)
    {
        int intVal = val ? 0 : 1;
        PlayerPrefs.SetInt("VibrateState", intVal);
    }
}