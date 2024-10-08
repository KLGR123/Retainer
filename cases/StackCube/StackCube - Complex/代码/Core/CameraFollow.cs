using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    [Range(0, 1)] [SerializeField] private float _smoothTime = 0.45f;
    [SerializeField] private float _offsetY = 2f;

    private Vector3 _currentVelocity;

    private void LateUpdate()
    {
        FollowTarget();
    }

    private void FollowTarget()
    {
        if(MovingCube.CurrentCube != null)
        {
            Vector3 targetPosition = new Vector3(transform.position.x, MovingCube.CurrentCube.transform.position.y + _offsetY, transform.position.z);
            transform.position = Vector3.SmoothDamp(transform.position, targetPosition, ref _currentVelocity, _smoothTime);
        }
    }
}
