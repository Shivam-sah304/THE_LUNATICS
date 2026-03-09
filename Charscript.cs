// using UnityEngine;

// [RequireComponent(typeof(CharacterController))]
// public class Charscript : MonoBehaviour
// {
//     [Header("Movement & Physics")]
//     public float walkSpeed = 5.0f;
//     public float rotationSpeed = 15.0f; 
//     public float jumpHeight = 1.5f; 
//     public float gravity = -20f;

//     [Header("Camera Settings")]
//     public Transform cameraBoom; 
//     public Camera mainCam;
//     public Vector3 standardCamOffset = new Vector3(0, 1.0f, -4.0f);
//     public Vector3 shoulderCamOffset = new Vector3(0.7f, 0.5f, -1.2f);
//     public float mouseSensitivity = 2.0f;

//     private CharacterController controller;
//     private Animator anim;
//     private float verticalVelocity;
//     private bool isAiming = false;
//     private float yaw = 0f;   
//     private float pitch = 0f; 

//     void Start()
//     {
//         controller = GetComponent<CharacterController>();
//         anim = GetComponent<Animator>();
//         if (mainCam == null) mainCam = Camera.main;
        
//         Cursor.lockState = CursorLockMode.Locked; 
//         yaw = transform.eulerAngles.y;
//     }

//     void Update()
//     {
//         HandleStates();
//         HandleCameraAndRotation();
//         HandleMovement();
//     }

//     void HandleStates()
//     {
//         if (Input.GetKeyDown(KeyCode.A) || Input.GetMouseButtonDown(1)) isAiming = !isAiming;
//         if (Input.GetKeyDown(KeyCode.Return)) anim.SetTrigger("FireTrigger");

//         float v = Input.GetAxis("Vertical");
//         float h = Input.GetAxis("Horizontal");
//         anim.SetBool("isMoving", (Mathf.Abs(v) > 0.1f || Mathf.Abs(h) > 0.1f));
//         anim.SetBool("isAiming", isAiming);
//     }

//     void HandleCameraAndRotation()
//     {
//         float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
//         float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;
//         float arrowH = Input.GetAxis("Horizontal");

//         // 1. MOUSE ALWAYS CONTROLS CAMERA ORBIT
//         yaw += mouseX;
//         pitch -= mouseY;
//         pitch = Mathf.Clamp(pitch, -30f, 60f); 

//         if (isAiming)
//         {
//             // AIM MODE: Left/Right arrows rotate ONLY the player body
//             // Camera (Yaw) stays constant relative to world
//             if (Mathf.Abs(arrowH) > 0.1f)
//             {
//                 transform.Rotate(0, arrowH * rotationSpeed * 10f * Time.deltaTime, 0);
//             }
//         }
//         else
//         {
//             // NORMAL MODE: Sync rotation
//             if (Mathf.Abs(arrowH) > 0.1f)
//             {
//                 float turnAmount = arrowH * rotationSpeed * 10f * Time.deltaTime;
//                 transform.Rotate(0, turnAmount, 0);
//                 yaw = transform.eulerAngles.y; // FORCE sync yaw to body rotation to stop flickering
//             }
//         }

//         // 2. APPLY TO BOOM (Pivot)
//         // This ensures the camera pivot always respects our manual yaw variable
//         cameraBoom.parent.rotation = Quaternion.Euler(0, yaw, 0);
//         cameraBoom.localRotation = Quaternion.Euler(pitch, 0, 0);

//         // 3. POSITION CAMERA (Shoulder Zoom)
//         Vector3 targetOffset = isAiming ? shoulderCamOffset : standardCamOffset;
//         mainCam.transform.localPosition = Vector3.Lerp(mainCam.transform.localPosition, targetOffset, Time.deltaTime * 7f);
//     }

//     void HandleMovement()
//     {
//         float v = Input.GetAxis("Vertical");
//         Vector3 moveDir = Vector3.zero;

//         // UP Arrow: Move toward camera focus
//         if (v > 0.1f) 
//         {
//             Vector3 camForward = cameraBoom.parent.forward;
//             camForward.y = 0;
//             moveDir = camForward.normalized;

//             // In Normal mode, ensure the body faces where the camera is looking
//             if (!isAiming)
//             {
//                 Quaternion targetRot = Quaternion.LookRotation(camForward);
//                 transform.rotation = Quaternion.Slerp(transform.rotation, targetRot, rotationSpeed * Time.deltaTime);
//                 // After the slerp, re-sync yaw one last time to prevent drift
//                 yaw = transform.eulerAngles.y; 
//             }
//         }
//         else if (v < -0.1f) 
//         {
//             moveDir = -transform.forward;
//         }

//         // PHYSICS
//         if (controller.isGrounded)
//         {
//             verticalVelocity = -2f; 
//             if (Input.GetButtonDown("Jump"))
//                 verticalVelocity = Mathf.Sqrt(jumpHeight * -2f * gravity);
//         }
//         else
//         {
//             verticalVelocity += gravity * Time.deltaTime;
//         }

//         Vector3 finalMove = moveDir * walkSpeed;
//         finalMove.y = verticalVelocity;
//         controller.Move(finalMove * Time.deltaTime);
//     }
// }



// using UnityEngine;

// [RequireComponent(typeof(CharacterController))]
// public class Charscript : MonoBehaviour
// {
//     [Header("Movement & Physics")]
//     public float walkSpeed = 5.0f;
//     public float rotationSpeed = 15.0f; 
//     public float jumpHeight = 1.5f; 
//     public float gravity = -20f;

//     [Header("Camera Settings")]
//     public Transform cameraBoom; 
//     public Camera mainCam;
//     public Vector3 standardCamOffset = new Vector3(0, 1.0f, -4.0f);
//     public Vector3 shoulderCamOffset = new Vector3(0.7f, 0.5f, -1.2f);
//     public float mouseSensitivity = 2.0f;

//     [Header("Gun & Projectile")]
//     public Transform spawnPoint;      // Drag your SpawnPoint object here
//     public GameObject bulletPrefab;   // Drag your Bullet Prefab here
//     public GameObject crosshairUI;    // Drag your UI Crosshair Image here
//     public float bulletSpeed = 50f;
//     public LayerMask aimLayers;       // Set this to "Everything" except "Player" layer

//     private CharacterController controller;
//     private Animator anim;
//     private float verticalVelocity;
//     private bool isAiming = false;
//     private float yaw = 0f;   
//     private float pitch = 0f; 

//     void Start()
//     {
//         controller = GetComponent<CharacterController>();
//         anim = GetComponent<Animator>();
//         if (mainCam == null) mainCam = Camera.main;
        
//         Cursor.lockState = CursorLockMode.Locked; 
//         yaw = transform.eulerAngles.y;

//         // Hide crosshair at start
//         if (crosshairUI != null) crosshairUI.SetActive(false);
//     }

//     void Update()
//     {
//         HandleStates();
//         HandleCameraAndRotation();
//         HandleMovement();
//     }

//     void HandleStates()
//     {
//         // Toggle Aiming
//         if (Input.GetKeyDown(KeyCode.A) || Input.GetMouseButtonDown(1))
//         {
//             isAiming = !isAiming;
//             if (crosshairUI != null) crosshairUI.SetActive(isAiming);
//         }

//         // Fire Projectile on Enter
//         if (Input.GetKeyDown(KeyCode.Return))
//         {
//             anim.SetTrigger("FireTrigger");
//             FireGun();
//         }

//         float v = Input.GetAxis("Vertical");
//         float h = Input.GetAxis("Horizontal");
//         anim.SetBool("isMoving", (Mathf.Abs(v) > 0.1f || Mathf.Abs(h) > 0.1f));
//         anim.SetBool("isAiming", isAiming);
//     }

//     void FireGun()
//     {
//         if (spawnPoint == null || bulletPrefab == null) return;

//         // 1. Raycast from Camera Center to find the target point
//         Ray ray = mainCam.ViewportPointToRay(new Vector3(0.5f, 0.5f, 0));
//         Vector3 targetPoint;
//         if (Physics.Raycast(ray, out RaycastHit hit, 100f, aimLayers))
//             targetPoint = hit.point;
//         else
//             targetPoint = ray.GetPoint(75f);

//         // 2. Direction from Barrel to Target
//         Vector3 fireDir = (targetPoint - spawnPoint.position).normalized;

//         // 3. Spawn Bullet
//         GameObject bullet = Instantiate(bulletPrefab, spawnPoint.position, Quaternion.LookRotation(fireDir));
        
//         // 4. Set Bullet Velocity
//         Rigidbody rb = bullet.GetComponent<Rigidbody>();
//         if (rb != null) rb.linearVelocity = fireDir * bulletSpeed;

//         Destroy(bullet, 3f);
//     }

//     void HandleCameraAndRotation()
//     {
//         float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
//         float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;
//         float arrowH = Input.GetAxis("Horizontal");

//         yaw += mouseX;
//         pitch -= mouseY;
//         pitch = Mathf.Clamp(pitch, -30f, 60f); 

//         if (isAiming)
//         {
//             if (Mathf.Abs(arrowH) > 0.1f)
//             {
//                 transform.Rotate(0, arrowH * rotationSpeed * 10f * Time.deltaTime, 0);
//             }
//         }
//         else
//         {
//             if (Mathf.Abs(arrowH) > 0.1f)
//             {
//                 float turnAmount = arrowH * rotationSpeed * 10f * Time.deltaTime;
//                 transform.Rotate(0, turnAmount, 0);
//                 yaw = transform.eulerAngles.y; 
//             }
//         }

//         cameraBoom.parent.rotation = Quaternion.Euler(0, yaw, 0);
//         cameraBoom.localRotation = Quaternion.Euler(pitch, 0, 0);

//         Vector3 targetOffset = isAiming ? shoulderCamOffset : standardCamOffset;
//         mainCam.transform.localPosition = Vector3.Lerp(mainCam.transform.localPosition, targetOffset, Time.deltaTime * 7f);
//     }

//     void HandleMovement()
//     {
//         float v = Input.GetAxis("Vertical");
//         Vector3 moveDir = Vector3.zero;

//         if (v > 0.1f) 
//         {
//             Vector3 camForward = cameraBoom.parent.forward;
//             camForward.y = 0;
//             moveDir = camForward.normalized;

//             if (!isAiming)
//             {
//                 Quaternion targetRot = Quaternion.LookRotation(camForward);
//                 transform.rotation = Quaternion.Slerp(transform.rotation, targetRot, rotationSpeed * Time.deltaTime);
//                 yaw = transform.eulerAngles.y; 
//             }
//         }
//         else if (v < -0.1f) 
//         {
//             moveDir = -transform.forward;
//         }

//         if (controller.isGrounded)
//         {
//             verticalVelocity = -2f; 
//             if (Input.GetButtonDown("Jump"))
//                 verticalVelocity = Mathf.Sqrt(jumpHeight * -2f * gravity);
//         }
//         else
//         {
//             verticalVelocity += gravity * Time.deltaTime;
//         }

//         Vector3 finalMove = moveDir * walkSpeed;
//         finalMove.y = verticalVelocity;
//         controller.Move(finalMove * Time.deltaTime);
//     }
// }



using UnityEngine;
using UnityEngine.UI; // Required for UI manipulation

[RequireComponent(typeof(CharacterController))]
public class Charscript : MonoBehaviour
{
    [Header("Movement & Physics")]
    public float walkSpeed = 5.0f;
    public float rotationSpeed = 15.0f; 
    public float jumpHeight = 1.5f; 
    public float gravity = -20f;

    [Header("Camera Settings")]
    public Transform cameraBoom; 
    public Camera mainCam;
    public Vector3 standardCamOffset = new Vector3(0, 1.0f, -4.0f);
    public Vector3 shoulderCamOffset = new Vector3(0.7f, 0.5f, -1.2f);
    public float mouseSensitivity = 2.0f;

    [Header("Gun & Projectile")]
    public Transform spawnPoint;      
    public GameObject bulletPrefab;   
    public GameObject crosshairUI;    // Your UI Image (Canvas)
    public GameObject aimSphere;      // Your 3D Sphere in the world
    public ParticleSystem muzzleFlash; 
    public float bulletSpeed = 50f;
    public float fireRate = 0.2f;      
    public LayerMask aimLayers;       

    private CharacterController controller;
    private Animator anim;
    private RectTransform crosshairRect; // For moving the UI Image
    private float verticalVelocity;
    private bool isAiming = false;
    private float nextFireTime = 0f;
    private float yaw = 0f;   
    private float pitch = 0f; 

    void Start()
    {
        controller = GetComponent<CharacterController>();
        anim = GetComponent<Animator>();
        if (mainCam == null) mainCam = Camera.main;
        
        // Setup Crosshair RectTransform
        if (crosshairUI != null) 
        {
            crosshairRect = crosshairUI.GetComponent<RectTransform>();
            crosshairUI.SetActive(false);
        }

        // Hide sphere's visual but keep it for math (optional)
        if (aimSphere != null && aimSphere.GetComponent<MeshRenderer>())
            aimSphere.GetComponent<MeshRenderer>().enabled = false;

        Cursor.lockState = CursorLockMode.Locked; 
        yaw = transform.eulerAngles.y;
    }

    void Update()
    {
        HandleStates();
        HandleCameraAndRotation();
        HandleMovement();
        UpdateDynamicCrosshair(); // New logic to link Gun -> Sphere -> UI
    }

    void HandleStates()
    {
        if (Input.GetKeyDown(KeyCode.A) || Input.GetMouseButtonDown(1))
        {
            isAiming = !isAiming;
            if (crosshairUI != null) crosshairUI.SetActive(isAiming);
        }

        if (Input.GetKeyDown(KeyCode.Return) && Time.time >= nextFireTime)
        {
            nextFireTime = Time.time + fireRate;
            anim.SetTrigger("FireTrigger");
            FireGun();
        }

        float v = Input.GetAxis("Vertical");
        float h = Input.GetAxis("Horizontal");
        anim.SetBool("isMoving", (Mathf.Abs(v) > 0.1f || Mathf.Abs(h) > 0.1f));
        anim.SetBool("isAiming", isAiming);
    }

    // This makes the UI crosshair follow the gun's physical direction
    void UpdateDynamicCrosshair()
    {
        if (isAiming && spawnPoint != null && aimSphere != null && crosshairRect != null)
        {
            RaycastHit hit;
            // Raycast from barrel forward
            if (Physics.Raycast(spawnPoint.position, spawnPoint.forward, out hit, 100f, aimLayers))
            {
                aimSphere.transform.position = hit.point;
            }
            else
            {
                aimSphere.transform.position = spawnPoint.position + (spawnPoint.forward * 100f);
            }

            // Convert 3D Sphere position to Screen Pixels
            Vector3 screenPos = mainCam.WorldToScreenPoint(aimSphere.transform.position);

            // Move UI Image to that pixel position
            if (screenPos.z > 0) // Only show if target is in front of camera
            {
                crosshairRect.gameObject.SetActive(true);
                crosshairRect.position = screenPos;
            }
            else
            {
                crosshairRect.gameObject.SetActive(false);
            }
        }
        else if (crosshairUI != null)
        {
            crosshairUI.SetActive(false);
        }
    }

    void FireGun()
    {
        if (spawnPoint == null || bulletPrefab == null) return;

        if (muzzleFlash != null) muzzleFlash.Play();

        // Direction is exactly where the barrel is pointing (aimSphere)
        Vector3 fireDir = (aimSphere.transform.position - spawnPoint.position).normalized;

        GameObject bullet = Instantiate(bulletPrefab, spawnPoint.position, Quaternion.LookRotation(fireDir));
        
        Rigidbody rb = bullet.GetComponent<Rigidbody>();
        if (rb != null) rb.linearVelocity = fireDir * bulletSpeed;

        Destroy(bullet, 3f);
    }

    void HandleCameraAndRotation()
    {
        float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
        float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;
        float arrowH = Input.GetAxis("Horizontal");

        yaw += mouseX;
        pitch -= mouseY;
        pitch = Mathf.Clamp(pitch, -30f, 60f); 

        if (isAiming)
        {
            if (Mathf.Abs(arrowH) > 0.1f)
            {
                transform.Rotate(0, arrowH * rotationSpeed * 10f * Time.deltaTime, 0);
            }
        }
        else
        {
            if (Mathf.Abs(arrowH) > 0.1f)
            {
                float turnAmount = arrowH * rotationSpeed * 10f * Time.deltaTime;
                transform.Rotate(0, turnAmount, 0);
                yaw = transform.eulerAngles.y; 
            }
        }

        if(cameraBoom.parent != null)
            cameraBoom.parent.rotation = Quaternion.Euler(0, yaw, 0);
            
        cameraBoom.localRotation = Quaternion.Euler(pitch, 0, 0);

        Vector3 targetOffset = isAiming ? shoulderCamOffset : standardCamOffset;
        mainCam.transform.localPosition = Vector3.Lerp(mainCam.transform.localPosition, targetOffset, Time.deltaTime * 7f);
    }

    void HandleMovement()
    {
        float v = Input.GetAxis("Vertical");
        Vector3 moveDir = Vector3.zero;

        if (v > 0.1f) 
        {
            Vector3 camForward = cameraBoom.parent.forward;
            camForward.y = 0;
            moveDir = camForward.normalized;

            if (!isAiming)
            {
                Quaternion targetRot = Quaternion.LookRotation(camForward);
                transform.rotation = Quaternion.Slerp(transform.rotation, targetRot, rotationSpeed * Time.deltaTime);
                yaw = transform.eulerAngles.y; 
            }
        }
        else if (v < -0.1f) 
        {
            moveDir = -transform.forward;
        }

        if (controller.isGrounded)
        {
            verticalVelocity = -2f; 
            if (Input.GetButtonDown("Jump"))
                verticalVelocity = Mathf.Sqrt(jumpHeight * -2f * gravity);
        }
        else
        {
            verticalVelocity += gravity * Time.deltaTime;
        }

        Vector3 finalMove = moveDir * walkSpeed;
        finalMove.y = verticalVelocity;
        controller.Move(finalMove * Time.deltaTime);
    }
}




// using UnityEngine;
// using UnityEngine.UI; // Required for UI manipulation

// [RequireComponent(typeof(CharacterController))]
// public class Charscript : MonoBehaviour
// {
//     [Header("Movement & Physics")]
//     public float walkSpeed = 5.0f;
//     public float rotationSpeed = 15.0f; 
//     public float jumpHeight = 1.5f; 
//     public float gravity = -20f;

//     [Header("Camera Settings")]
//     public Transform cameraBoom; 
//     public Camera mainCam;
//     public Vector3 standardCamOffset = new Vector3(0, 1.0f, -4.0f);
//     public Vector3 shoulderCamOffset = new Vector3(0.7f, 0.5f, -1.2f);
//     public float mouseSensitivity = 2.0f;

//     [Header("Gun & Projectile")]
//     public Transform spawnPoint;      
//     public GameObject bulletPrefab;   
//     public GameObject crosshairUI;    // Your UI Image (Canvas)
//     public GameObject aimSphere;      // Your 3D Sphere in the world
//     public ParticleSystem muzzleFlash; 
//     public float bulletSpeed = 50f;
//     public float fireRate = 0.2f;      
//     public LayerMask aimLayers;       

//     private CharacterController controller;
//     private Animator anim;
//     private RectTransform crosshairRect; // For moving the UI Image
//     private float verticalVelocity;
//     private bool isAiming = false;
//     private float nextFireTime = 0f;
//     private float yaw = 0f;   
//     private float pitch = 0f; 

//     void Start()
//     {
//         controller = GetComponent<CharacterController>();
//         anim = GetComponent<Animator>();
//         if (mainCam == null) mainCam = Camera.main;
        
//         // Setup Crosshair RectTransform
//         if (crosshairUI != null) 
//         {
//             crosshairRect = crosshairUI.GetComponent<RectTransform>();
//             crosshairUI.SetActive(false);
//         }

//         // Hide sphere's visual but keep it for math (optional)
//         if (aimSphere != null && aimSphere.GetComponent<MeshRenderer>())
//             aimSphere.GetComponent<MeshRenderer>().enabled = false;

//         Cursor.lockState = CursorLockMode.Locked; 
//         yaw = transform.eulerAngles.y;
//     }

//     void Update()
//     {
//         HandleStates();
//         HandleCameraAndRotation();
//         HandleMovement();
//         UpdateDynamicCrosshair(); // New logic to link Gun -> Sphere -> UI
//     }

//     void HandleStates()
//     {
//         if (Input.GetKeyDown(KeyCode.A) || Input.GetMouseButtonDown(1))
//         {
//             isAiming = !isAiming;
//             if (crosshairUI != null) crosshairUI.SetActive(isAiming);
//         }

//         if (Input.GetKeyDown(KeyCode.Return) && Time.time >= nextFireTime)
//         {
//             nextFireTime = Time.time + fireRate;
//             anim.SetTrigger("FireTrigger");
//             FireGun();
//         }

//         float v = Input.GetAxis("Vertical");
//         float h = Input.GetAxis("Horizontal");
//         anim.SetBool("isMoving", (Mathf.Abs(v) > 0.1f || Mathf.Abs(h) > 0.1f));
//         anim.SetBool("isAiming", isAiming);
//     }

//     // This makes the UI crosshair follow the gun's physical direction
//     void UpdateDynamicCrosshair()
//     {
//         if (isAiming && spawnPoint != null && aimSphere != null && crosshairRect != null)
//         {
//             RaycastHit hit;
//             // Raycast from barrel forward
//             if (Physics.Raycast(spawnPoint.position, spawnPoint.forward, out hit, 100f, aimLayers))
//             {
//                 aimSphere.transform.position = hit.point;
//             }
//             else
//             {
//                 aimSphere.transform.position = spawnPoint.position + (spawnPoint.forward * 100f);
//             }

//             // Convert 3D Sphere position to Screen Pixels
//             Vector3 screenPos = mainCam.WorldToScreenPoint(aimSphere.transform.position);

//             // Move UI Image to that pixel position
//             if (screenPos.z > 0) // Only show if target is in front of camera
//             {
//                 crosshairRect.gameObject.SetActive(true);
//                 crosshairRect.position = screenPos;
//             }
//             else
//             {
//                 crosshairRect.gameObject.SetActive(false);
//             }
//         }
//         else if (crosshairUI != null)
//         {
//             crosshairUI.SetActive(false);
//         }
//     }

//     void FireGun()
//     {
//         if (spawnPoint == null || bulletPrefab == null) return;

//         if (muzzleFlash != null) muzzleFlash.Play();

//         // Direction is exactly where the barrel is pointing (aimSphere)
//         Vector3 fireDir = (aimSphere.transform.position - spawnPoint.position).normalized;

//         GameObject bullet = Instantiate(bulletPrefab, spawnPoint.position, Quaternion.LookRotation(fireDir));
        
//         Rigidbody rb = bullet.GetComponent<Rigidbody>();
//         if (rb != null) rb.linearVelocity = fireDir * bulletSpeed;

//         Destroy(bullet, 3f);
//     }

//     void HandleCameraAndRotation()
//     {
//         float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
//         float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;
//         float arrowH = Input.GetAxis("Horizontal");

//         yaw += mouseX;
//         pitch -= mouseY;
//         pitch = Mathf.Clamp(pitch, -30f, 60f); 

//         if (isAiming)
//         {
//             if (Mathf.Abs(arrowH) > 0.1f)
//             {
//                 transform.Rotate(0, arrowH * rotationSpeed * 10f * Time.deltaTime, 0);
//             }
//         }
//         else
//         {
//             if (Mathf.Abs(arrowH) > 0.1f)
//             {
//                 float turnAmount = arrowH * rotationSpeed * 10f * Time.deltaTime;
//                 transform.Rotate(0, turnAmount, 0);
//                 yaw = transform.eulerAngles.y; 
//             }
//         }

//         if(cameraBoom.parent != null)
//             cameraBoom.parent.rotation = Quaternion.Euler(0, yaw, 0);
            
//         cameraBoom.localRotation = Quaternion.Euler(pitch, 0, 0);

//         Vector3 targetOffset = isAiming ? shoulderCamOffset : standardCamOffset;
//         mainCam.transform.localPosition = Vector3.Lerp(mainCam.transform.localPosition, targetOffset, Time.deltaTime * 7f);
//     }

//     void HandleMovement()
//     {
//         float v = Input.GetAxis("Vertical");
//         Vector3 moveDir = Vector3.zero;

//         if (v > 0.1f) 
//         {
//             Vector3 camForward = cameraBoom.parent.forward;
//             camForward.y = 0;
//             moveDir = camForward.normalized;

//             if (!isAiming)
//             {
//                 Quaternion targetRot = Quaternion.LookRotation(camForward);
//                 transform.rotation = Quaternion.Slerp(transform.rotation, targetRot, rotationSpeed * Time.deltaTime);
//                 yaw = transform.eulerAngles.y; 
//             }
//         }
//         else if (v < -0.1f) 
//         {
//             moveDir = -transform.forward;
//         }

//         if (controller.isGrounded)
//         {
//             verticalVelocity = -2f; 
//             if (Input.GetButtonDown("Jump"))
//                 verticalVelocity = Mathf.Sqrt(jumpHeight * -2f * gravity);
//         }
//         else
//         {
//             verticalVelocity += gravity * Time.deltaTime;
//         }

//         Vector3 finalMove = moveDir * walkSpeed;
//         finalMove.y = verticalVelocity;
//         controller.Move(finalMove * Time.deltaTime);
//     }
// }





// using UnityEngine;
// using UnityEngine.UI;

// [RequireComponent(typeof(CharacterController))]
// public class Charscript : MonoBehaviour
// {
//     [Header("Movement & Physics")]
//     public float walkSpeed = 5.0f;
//     public float rotationSpeed = 15.0f; 
//     public float jumpHeight = 1.5f; 
//     public float gravity = -20f;

//     [Header("Camera Settings")]
//     public Transform cameraBoom; 
//     public Camera mainCam;
//     public Vector3 standardCamOffset = new Vector3(0, 1.0f, -4.0f);
//     public Vector3 shoulderCamOffset = new Vector3(0.7f, 0.5f, -1.2f);
//     public float mouseSensitivity = 2.0f;

//     [Header("Gun & Projectile")]
//     public Transform spawnPoint;      
//     public GameObject bulletPrefab;   
//     public GameObject crosshairUI;    
//     public GameObject aimSphere;      
//     public ParticleSystem muzzleFlash; 
//     public float bulletSpeed = 50f;
//     public float fireRate = 0.2f;      
//     public LayerMask aimLayers;       

//     [Header("Procedural Aiming (Manual)")]
//     public Transform spineBone;       // Drag character's Spine/Chest bone here
//     public Vector3 aimOffset;         // Use this to fix crooked gun angles

//     private CharacterController controller;
//     private Animator anim;
//     private RectTransform crosshairRect; 
//     private float verticalVelocity;
//     private bool isAiming = false;
//     private float nextFireTime = 0f;
//     private float yaw = 0f;   
//     private float pitch = 0f; 

//     void Start()
//     {
//         controller = GetComponent<CharacterController>();
//         anim = GetComponent<Animator>();
//         if (mainCam == null) mainCam = Camera.main;
        
//         if (crosshairUI != null) 
//         {
//             crosshairRect = crosshairUI.GetComponent<RectTransform>();
//             crosshairUI.SetActive(false);
//         }

//         if (aimSphere != null && aimSphere.GetComponent<MeshRenderer>())
//             aimSphere.GetComponent<MeshRenderer>().enabled = false;

//         Cursor.lockState = CursorLockMode.Locked; 
//         yaw = transform.eulerAngles.y;
//     }

//     void Update()
//     {
//         HandleStates();
//         HandleCameraAndRotation();
//         HandleMovement();
//         UpdateDynamicCrosshair(); 
//     }

//     // LateUpdate is essential for manual bone rotation
//     void LateUpdate()
//     {
//         if (isAiming && spineBone != null)
//         {
//             // Rotate the spine based on the camera pitch
//             // Adjust the axis (X, Y, or Z) based on your character's rig
//             spineBone.localRotation *= Quaternion.Euler(-pitch, 0, 0);
//             spineBone.localRotation *= Quaternion.Euler(aimOffset);
//         }
//     }

//     void HandleStates()
//     {
//         // Toggle Aiming with 'A' or Right Click
//         if (Input.GetKeyDown(KeyCode.A) || Input.GetMouseButtonDown(1))
//         {
//             isAiming = !isAiming;
//             if (crosshairUI != null) crosshairUI.SetActive(isAiming);
//         }

//         if (Input.GetKeyDown(KeyCode.Return) && Time.time >= nextFireTime)
//         {
//             nextFireTime = Time.time + fireRate;
//             anim.SetTrigger("FireTrigger");
//             FireGun();
//         }

//         float v = Input.GetAxis("Vertical");
//         float h = Input.GetAxis("Horizontal");
//         anim.SetBool("isMoving", (Mathf.Abs(v) > 0.1f || Mathf.Abs(h) > 0.1f));
//         anim.SetBool("isAiming", isAiming);
//     }

//     void UpdateDynamicCrosshair()
//     {
//         if (isAiming && spawnPoint != null && aimSphere != null && crosshairRect != null)
//         {
//             RaycastHit hit;
//             if (Physics.Raycast(spawnPoint.position, spawnPoint.forward, out hit, 100f, aimLayers))
//                 aimSphere.transform.position = hit.point;
//             else
//                 aimSphere.transform.position = spawnPoint.position + (spawnPoint.forward * 100f);

//             Vector3 screenPos = mainCam.WorldToScreenPoint(aimSphere.transform.position);

//             if (screenPos.z > 0) 
//             {
//                 crosshairRect.gameObject.SetActive(true);
//                 crosshairRect.position = screenPos;
//             }
//             else crosshairRect.gameObject.SetActive(false);
//         }
//         else if (crosshairUI != null) crosshairUI.SetActive(false);
//     }

//     void FireGun()
//     {
//         if (spawnPoint == null || bulletPrefab == null) return;
//         if (muzzleFlash != null) muzzleFlash.Play();

//         Vector3 fireDir = (aimSphere.transform.position - spawnPoint.position).normalized;
//         GameObject bullet = Instantiate(bulletPrefab, spawnPoint.position, Quaternion.LookRotation(fireDir));
        
//         Rigidbody rb = bullet.GetComponent<Rigidbody>();
//         if (rb != null) rb.linearVelocity = fireDir * bulletSpeed;

//         Destroy(bullet, 3f);
//     }

//     void HandleCameraAndRotation()
//     {
//         yaw += Input.GetAxis("Mouse X") * mouseSensitivity;
//         pitch -= Input.GetAxis("Mouse Y") * mouseSensitivity;
//         pitch = Mathf.Clamp(pitch, -30f, 60f); 

//         float arrowH = Input.GetAxis("Horizontal");

//         if (isAiming)
//         {
//             // Body faces camera direction while aiming
//             transform.rotation = Quaternion.Euler(0, yaw, 0);

//             if (Mathf.Abs(arrowH) > 0.1f)
//             {
//                 transform.Rotate(0, arrowH * rotationSpeed * 10f * Time.deltaTime, 0);
//                 yaw = transform.eulerAngles.y; 
//             }
//         }
//         else
//         {
//             if (Mathf.Abs(arrowH) > 0.1f)
//             {
//                 float turnAmount = arrowH * rotationSpeed * 10f * Time.deltaTime;
//                 transform.Rotate(0, turnAmount, 0);
//                 yaw = transform.eulerAngles.y; 
//             }
//         }

//         if(cameraBoom.parent != null)
//             cameraBoom.parent.rotation = Quaternion.Euler(0, yaw, 0);
            
//         cameraBoom.localRotation = Quaternion.Euler(pitch, 0, 0);

//         Vector3 targetOffset = isAiming ? shoulderCamOffset : standardCamOffset;
//         mainCam.transform.localPosition = Vector3.Lerp(mainCam.transform.localPosition, targetOffset, Time.deltaTime * 7f);
//     }

//     void HandleMovement()
//     {
//         float v = Input.GetAxis("Vertical");
//         Vector3 moveDir = Vector3.zero;

//         if (v > 0.1f) 
//         {
//             Vector3 camForward = cameraBoom.parent.forward;
//             camForward.y = 0;
//             moveDir = camForward.normalized;

//             if (!isAiming)
//             {
//                 Quaternion targetRot = Quaternion.LookRotation(camForward);
//                 transform.rotation = Quaternion.Slerp(transform.rotation, targetRot, rotationSpeed * Time.deltaTime);
//                 yaw = transform.eulerAngles.y; 
//             }
//         }
//         else if (v < -0.1f) moveDir = -transform.forward;

//         if (controller.isGrounded)
//         {
//             verticalVelocity = -2f; 
//             if (Input.GetButtonDown("Jump"))
//                 verticalVelocity = Mathf.Sqrt(jumpHeight * -2f * gravity);
//         }
//         else verticalVelocity += gravity * Time.deltaTime;

//         Vector3 finalMove = moveDir * walkSpeed;
//         finalMove.y = verticalVelocity;
//         controller.Move(finalMove * Time.deltaTime);
//     }
// }
