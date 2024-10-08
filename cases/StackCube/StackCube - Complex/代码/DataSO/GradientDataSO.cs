using UnityEngine;

[CreateAssetMenu(menuName = "SO/Gradient Data", fileName = "Gradient Data")]
public class GradientDataSO : ScriptableObject
{
    [SerializeField] Gradient[] _gradientList;

    public Gradient[] GradientList => _gradientList;

}

[System.Serializable]
public class Gradient
{
    public Color[] colour;
}
