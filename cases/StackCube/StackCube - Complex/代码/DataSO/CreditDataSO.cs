using UnityEngine;

[CreateAssetMenu(menuName = "SO/Credit Data", fileName = "Credit Data")]
public class CreditDataSO : ScriptableObject
{
    [Space]
    [SerializeField] [TextArea(2, 2)] string _title;

    [Header("Description :")]
    [SerializeField] [TextArea(4, 6)] string _desc;

    public string GetTitle => _title;
    public string GetDesc => _desc;
}
