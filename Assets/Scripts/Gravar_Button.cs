using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Gravar_Button : MonoBehaviour
{
    public Button record;
    public string question;
    // Start is called before the first frame update
    void Start()
    {
        record.onClick.AddListener(delegate { recordQuestion(question); });
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void recordQuestion(string question)
    {
        
    }
}
