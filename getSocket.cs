using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.Serialization;
using System.Text;
using System.Threading;
using UnityEngine;
using UnityEngine.UI;


public class getSocket: MonoBehaviour
{

    public Text text;
    private string message;
    private Socket client;
    private string host = "127.0.0.1";
    private int port = 10087;
    public byte[] messTmp;
    // Start is called before the first frame update
    void Start()
    {
        text = this.GetComponent<Text>();
        messTmp = new byte[1024];

        // 构建一个Socket实例，并连接指定的服务端。这里需要使用IPEndPoint类(ip和端口号的封装)
        client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        try
        {
            client.Connect(new IPEndPoint(IPAddress.Parse(host), port));
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            return;
        }

        //client.Close();
    }

    Data ReadToObject(string json)
    {
        
        Data deserializedUser = new Data();
        Debug.Log(json);
        deserializedUser = (Data)JsonUtility.FromJson(json, deserializedUser.GetType());
        return deserializedUser;
    }

    void GetMessage()
    {
        var count = client.Receive(messTmp);

        if (count != 0)
        {
            Data frame = ReadToObject(Encoding.UTF8.GetString(messTmp, 1, count - 2));
            message = frame.ToString();
            string r = frame.GetRange();
            string l = frame.GetList();
            Debug.Log("r = " + r);
            Debug.Log("l = " + l);
            Array.Clear(messTmp, 0, count);
        }
    }

    void FixedUpdate()
    {
        GetMessage();
        text.text = message;
    }

    // Update is called once per frame
    void Update()
    {

    }
}

[Serializable]
class Data
{
    public List<Frame> infolist;
    public List<DataField> rangelist;
    public override string ToString()
    {
        string tmp = "";
        foreach (DataField one in rangelist)
        {
            tmp += one.ToString() + "\n";
        }

        return tmp;
    }

    public string GetList()
    {
        string tmp = "";
        foreach (Frame one in infolist)
        {
            tmp += one + "\n";
        }

        return tmp;
    }
    public string GetRange()
    {
        string tmp = "";
        foreach (DataField one in rangelist)
        {
            tmp += one.ToString() + "\n";
        }

        return tmp;
    }
}

[Serializable]
class Frame
{
    public string name;
    public string age;

    public override string ToString()
    {
        return "name: " + name + " age: " + age;
    }
}

[Serializable]
class DataField
{
    public string tone;
    public string[] range;

    public override string ToString()
    {
        return "tone: " + tone + " range: " + range[0] +", "+ range[1];
    }
}


