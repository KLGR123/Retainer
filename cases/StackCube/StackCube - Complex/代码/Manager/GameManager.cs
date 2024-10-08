using System;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class GameManager : MonoBehaviour
{
    public static event Action OnGameStart;
    public static event Action OnGameEnd;

    [SerializeField] Material _skybox;
    [SerializeField] GradientDataSO _colorData;
    [SerializeField] Image _gradentImage;

    private int _spawnerIndex;
    private bool _firstSpawn = false;
    private CubeSpawner[] _spawners;
    private CubeSpawner _currentSpawner;

    private void Awake()
    {
        _spawners = FindObjectsOfType<CubeSpawner>();
    }

    private void Start()
    {
        if (MenuManager.Instance.GetCurrentMenu == MenuType.Gameplay)
            SpawnCube();

        SetBackgroundColor();
    }

    private void SetBackgroundColor()
    {
        int colorIndex = UnityEngine.Random.Range(0, _colorData.GradientList.Length);
        _skybox.SetColor("_Top", _colorData.GradientList[colorIndex].colour[0]);
        _skybox.SetColor("_Bottom", _colorData.GradientList[colorIndex].colour[1]);
        _gradentImage.color = _colorData.GradientList[colorIndex].colour[1];
    }

    private void Update()
    {
#if UNITY_EDITOR
        GetInput();
#endif

#if UNITY_ANDROID|| UNITY_WEBGL
        GetMobileInput();
#endif
    }

    private void GetMobileInput()
    {
        if (Input.touchCount > 0)
        {
            Touch touch = Input.touches[0];
            if (touch.phase == TouchPhase.Began && !EventSystem.current.IsPointerOverGameObject(touch.fingerId))
            {
                SpawnCube();
            }
        }
    }

    private void GetInput()
    {
        if (Input.GetMouseButtonDown(0) && !EventSystem.current.IsPointerOverGameObject())
        {
            SpawnCube();
        }
    }

    private void SpawnCube()
    {
        if (MovingCube.CurrentCube == null) return;

        if (!_firstSpawn)
        {
            _firstSpawn = true;
            OnGameStart?.Invoke();

            if (MenuManager.Instance.GetCurrentMenu != MenuType.Gameplay)
            {
                MenuManager.Instance.SwitchMenu(MenuType.Gameplay);
            }
        }

        bool isGameOver = MovingCube.CurrentCube.Stop();

        if (!isGameOver)
        {
            _spawnerIndex = _spawnerIndex == 0 ? 1 : 0;
            _currentSpawner = _spawners[_spawnerIndex];
            _currentSpawner.SpawnCube();
        }
        else
        {
            OnGameEnd?.Invoke();
            MenuManager.Instance.SwitchMenu(MenuType.GameOver);

            SoundManager.Instance.PlayAudio(AudioType.GAMEOVER);
            VibrationManager.Instance.StartVibration();
        }
    }
}
