using System.IO;
using UnityEngine;
using UnityEngine.UI;

public class RecordButton : MonoBehaviour
{
    private Button recordButton;
    private bool buttonPressed;
    private float startTime;
    // Start is called before the first frame update
    void Start()
    {
        recordButton = GetComponent<Button>();
        recordButton.onClick.AddListener(Record);
        buttonPressed = false;
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void Record()
    {
        AudioSource audioSource = GetComponent<AudioSource>();
        if(Microphone.devices.Length <= 0)
        {
            Debug.Log("I don't have microphones to record");
            return;
        }
        if(!buttonPressed)
        {
            Debug.Log("I'm recording. I have microphone " + Microphone.devices.Length);
            audioSource.clip = Microphone.Start(Microphone.devices[0], false, 3599, 44100);
            buttonPressed = true;
            startTime = Time.realtimeSinceStartup;
        }
        else
        {
            Microphone.End(null);
            float clipLength = Time.realtimeSinceStartup - startTime;
            int samples = (int)(audioSource.clip.frequency * clipLength);
            float[] data = new float[samples];
            audioSource.clip.GetData(data, 0);
            AudioClip trimmedClip = AudioClip.Create(audioSource.clip.name, samples, audioSource.clip.channels, audioSource.clip.frequency, false);
            trimmedClip.SetData(data, 0);
            if(trimmedClip != null)
            {
                SavWav.Save("Questions/CurrentQuestion.wav", trimmedClip);
            }
            buttonPressed = false;
        }
    }
}
