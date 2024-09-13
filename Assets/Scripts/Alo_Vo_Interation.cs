using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class Alo_Vo_Interation : MonoBehaviour
{
    private string URL = "";
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        Debug.Log("hello");
        StartCoroutine(GetAnswer());
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    IEnumerator GetAnswer()
    {
        Debug.Log("Oi in answer!");
        if(URL != "")
        {
            using(UnityWebRequest request = UnityWebRequest.Get(URL))
            {
                yield return request.SendWebRequest();
                
                if(request.result == UnityWebRequest.Result.ConnectionError)
                    Debug.LogError(request.error);
                else
                {
                    string json = request.downloadHandler.text;
                    Debug.Log(json);
                }
            }
        }
    }
}
