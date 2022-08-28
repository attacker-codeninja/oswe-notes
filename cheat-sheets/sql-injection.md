# SQL Injection

## SQL Injection Types

|    Type        | Description                     
|----------------|-------------------------------|
|In-band SQLi (Classic SQLi)|In-band SQL Injection is the most common and easy-to-exploit of SQL Injection attacks. In-band SQL Injection occurs when an attacker is able to use the same communication channel to both launch the attack and gather results. The two most common types of in-band SQL Injection are Error-based SQLi and Union-based SQLi. |    
|Error-based SQLi          |Error-based SQLi is an in-band SQL Injection technique that relies on error messages thrown by the database server to obtain information about the structure of the database. In some cases, error-based SQL injection alone is enough for an attacker to enumerate an entire database.| 
|Union-based SQLi         |Union-based SQLi is an in-band SQL injection technique that leverages the UNION SQL operator to combine the results of two or more SELECT statements into a single result which is then returned as part of the HTTP response.|
|Inferential SQLi (Blind SQLi)|Inferential SQL Injection, unlike in-band SQLi, may take longer for an attacker to exploit, however, it is just as dangerous as any other form of SQL Injection. In an inferential SQLi attack, no data is actually transferred via the web application and the attacker would not be able to see the result of an attack in-band (which is why such attacks are commonly referred to as “blind SQL Injection attacks”). Instead, an attacker is able to reconstruct the database structure by sending payloads, observing the web application’s response and the resulting behavior of the database server. The two types of inferential SQL Injection are Blind-boolean-based SQLi and Blind-time-based SQLi.|
|Boolean-based (content-based) Blind SQLi |Boolean-based SQL Injection is an inferential SQL Injection technique that relies on sending an SQL query to the database which forces the application to return a different result depending on whether the query returns a TRUE or FALSE result. Depending on the result, the content within the HTTP response will change, or remain the same. This allows an attacker to infer if the payload used returned true or false, even though no data from the database is returned.|
|Time-based Blind SQLi |Time-based SQL Injection is an inferential SQL Injection technique that relies on sending an SQL query to the database which forces the database to wait for a specified amount of time (in seconds) before responding. The response time will indicate to the attacker whether the result of the query is TRUE or FALSE. Depending on the result, an HTTP response will be returned with a delay, or returned immediately. This allows an attacker to infer if the payload used returned true or false, even though no data from the database is returned.|
|Out-of-band SQLi|Out-of-band SQL Injection is not very common, mostly because it depends on features being enabled on the database server being used by the web application. Out-of-band SQL Injection occurs when an attacker is unable to use the same channel to launch the attack and gather results. Out-of-band techniques, offer an attacker an alternative to inferential time-based techniques, especially if the server responses are not very stable (making an inferential time-based attack unreliable).|
| Voice Based Sql Injection | It is a sql injection attack method that can be applied in applications that provide access to databases with voice command. An attacker could pull information from the database by sending sql queries with sound. |

### Blind SQLi

- It is good practice to convert the resultant character to its numeric ASCII value and then perform the comparison e.g. `select/**/ascii(substring((select/**/version()),1,1))=52;`
  * `range(32, 126)` represents all printable characters:
```
    0 NUL    16 DLE    32      48 0    64 @    80 P    96 `   112 p 
    1 SOH    17 DC1    33 !    49 1    65 A    81 Q    97 a   113 q 
    2 STX    18 DC2    34 "    50 2    66 B    82 R    98 b   114 r 
    3 ETX    19 DC3    35 #    51 3    67 C    83 S    99 c   115 s 
    4 EOT    20 DC4    36 $    52 4    68 D    84 T   100 d   116 t 
    5 ENQ    21 NAK    37 %    53 5    69 E    85 U   101 e   117 u 
    6 ACK    22 SYN    38 &    54 6    70 F    86 V   102 f   118 v 
    7 BEL    23 ETB    39 '    55 7    71 G    87 W   103 g   119 w 
    8 BS     24 CAN    40 (    56 8    72 H    88 X   104 h   120 x 
    9 HT     25 EM     41 )    57 9    73 I    89 Y   105 i   121 y 
   10 LF     26 SUB    42 *    58 :    74 J    90 Z   106 j   122 z 
   11 VT     27 ESC    43 +    59 ;    75 K    91 [   107 k   123 { 
   12 FF     28 FS     44 ,    60 <    76 L    92 \   108 l   124 | 
   13 CR     29 GS     45 -    61 =    77 M    93 ]   109 m   125 } 
   14 SO     30 RS     46 .    62 >    78 N    94 ^   110 n   126 ~ 
   15 SI     31 US     47 /    63 ?    79 O    95 _   111 o   127 DEL
```

### Whitespace WAF-based bypass

Whenever the WAF blocks the query to include space/whitespace, you can easy replace with the following payloads:  

```
/**/
/**_**/
%23nuLL%0A
%23qa%0A%23%0A
%23foo*%2F*bar%0D%0A
+
```

For example, you can replace the whitespaces on the following payload:  
```http://domain.com/index.php?id=1' order by 1-- -```  
with  
```http://domain.com/index.php?id=1'/**/order/**/by/**/1--/**/-```  
or with  
```http://domain.com/index.php?id=1'%23nuLL%0Aorder%23nuLL%0Aby%23nuLL%0A1--%23nuLL%0A-```  
and so on...

### Whitespace Bypass via Emoji

```
/*️*/
/*️⃣*/
```
