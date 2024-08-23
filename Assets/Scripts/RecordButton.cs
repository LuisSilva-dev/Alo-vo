using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class RecordButton : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        GetComponent<Button>().onClick.AddListener(Record);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void Record()
    {
        if(Microphone.devices.Length <= 0)
        {
            Debug.Log("I don't have microphones to record");
        }
        else
        {
            Debug.Log("I'm recording.");
            AudioSource audioSource = GetComponent<AudioSource>();
            audioSource.clip = Microphone.Start("Built-in Microphone", true, 10, 44100);
            audioSource.Play();
        }
    }
}
