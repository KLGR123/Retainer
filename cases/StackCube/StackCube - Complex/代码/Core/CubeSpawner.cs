using System;
using UnityEngine;

public class CubeSpawner : MonoBehaviour
{
    public static int CubeCount;

    [SerializeField] private MovingCube _cubePrefab;
    [SerializeField] private MoveDirection _moveDirection;
    [SerializeField] private float _initialSpeed;
    [SerializeField] private float _maxSpeed;
    [SerializeField] private float _speedMultiplier = .05f;

    private float _currentSpeed;

    private void Awake()
    {
        CubeCount = 0;
        _currentSpeed = _initialSpeed;
    }

    public void SpawnCube()
    {
        var cube = Instantiate(_cubePrefab, transform);

        float x = _moveDirection == MoveDirection.X ? transform.position.x : MovingCube.LastCube.transform.position.x;
        float z = _moveDirection == MoveDirection.Z ? transform.position.z : MovingCube.LastCube.transform.position.z;

        cube.transform.position = new Vector3(x, MovingCube.LastCube.transform.position.y + _cubePrefab.transform.localScale.y, z);
        cube.MoveDirection = _moveDirection;

        CubeCount++;

        cube.SetSpeed(GetSpeed());
    }

    private float GetSpeed()
    {
        float additionalSpeed = CubeCount * _speedMultiplier;
        _currentSpeed = _initialSpeed + additionalSpeed;
        _currentSpeed = Mathf.Clamp(_currentSpeed, _initialSpeed, _maxSpeed);
        return _currentSpeed;
    }

    private void OnDestroy()
    {
        CubeCount = 0;
    }

    private void OnDrawGizmos()
    {
        Gizmos.color = Color.green;
        Gizmos.DrawWireCube(transform.position, _cubePrefab.transform.localScale);
    }
}
