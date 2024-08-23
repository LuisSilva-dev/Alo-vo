using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class OpenOverlay : MonoBehaviour
{
    public GameObject overlayBackground;
    private bool switchOn;
    // Start is called before the first frame update
    void Start()
    {
        switchOn = false;
        overlayBackground.SetActive(switchOn);
        GetComponent<Button>().onClick.AddListener(PressOverlay);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void PressOverlay()
    {
        switchOn = !switchOn;
        overlayBackground.SetActive(switchOn);
    }
}
