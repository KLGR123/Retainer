using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridManager : MonoBehaviour {

    public GameObject molePrefab;
    public int gridRows = 3;
    public int gridColumns = 3;
    public float xOffset = 1.5f;
    public float yOffset = 1.5f;

    private GameObject[,] grid;

    void Start()
    {
        grid = new GameObject[gridRows, gridColumns];
        CreateGrid();
    }

    void CreateGrid()
    {
        for (int i = 0; i < gridRows; i++)
        {
            for (int j = 0; j < gridColumns; j++)
            {
                Vector3 position = new Vector3(i * xOffset, j * yOffset, 0);
                grid[i, j] = Instantiate(molePrefab, position, Quaternion.identity);
                grid[i, j].transform.SetParent(transform);
            }
        }
    }
}