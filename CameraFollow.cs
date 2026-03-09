using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    public Transform target;           // Drag your Player here
    public float distance = 7.0f;      // How far away from player
    public float sensitivity = 3.0f;   // Mouse speed
    
    public float minY = -20f;          // Limit looking down
    public float maxY = 80f;           // Limit looking up

    private float currentX = 0.0f;     // Horizontal rotation
    private float currentY = 20.0f;    // Vertical rotation (start slightly tilted)

    void Start()
    {
        // Optional: Locks cursor to center of screen while playing
        Cursor.lockState = CursorLockMode.Locked;
    }

    void LateUpdate()
    {
        if (target != null)
        {
            // 1. Get Mouse Input
            currentX += Input.GetAxis("Mouse X") * sensitivity;
            currentY -= Input.GetAxis("Mouse Y") * sensitivity;

            // 2. Clamp the vertical angle so the camera doesn't flip upside down
            currentY = Mathf.Clamp(currentY, minY, maxY);

            // 3. Calculate Rotation and Position
            Quaternion rotation = Quaternion.Euler(currentY, currentX, 0);
            
            // Move the camera back by 'distance' from the target position
            Vector3 direction = new Vector3(0, 0, -distance);
            Vector3 position = target.position + rotation * direction;

            // 4. Update Camera
            transform.position = position;
            transform.LookAt(target.position + Vector3.up * 1.5f); // Look at player's head area
        }
        
        // Press Escape to free the mouse cursor
        if (Input.GetKeyDown(KeyCode.Escape))
            Cursor.lockState = CursorLockMode.None;
    }
}

