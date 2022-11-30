# My OSWE Journey

Time for OSWE I guess.

* **07/08/2022**: Journey begins

# Cheat Sheets

[Fundamentals](#fundamentals)

[Methodology](/cheat-sheets/methodology.md)

[MySQL](/cheat-sheets/mysql.md)

[PHP](/cheat-sheets/php.md)

[PostgreSQL](/cheat-sheets/postgresql.md)

[SQL Injection](/cheat-sheets/sql-injection.md)

# Fundamentals

## Tools

#### General

- [x] [CyberChef](https://gchq.github.io/CyberChef/) A web app for encryption, encoding, compression and data analysis
- [x] [JSNICE](http://jsnice.org/) A JavaScript Deobfuscation tool
- [x] [boxentriq/code-breaking](https://www.boxentriq.com/code-breaking) Various codebreaking and cipher tools
- [x] [regex101](https://regex101.com/) / [Learn Regex](https://regexr.com/) Regex testers

#### Decompilers

- [x] [dnSPY](https://github.com/dnSpy/dnSpy) .NET decompiler/debugger
- [x] [JD-GUI](http://java-decompiler.github.io/) Java decompiler

## Debuggers

<details><summary>Debugging Context Controls</summary>
<p>

- Continue: Application will resume execution until it completes or hits another breakpoint.
- Step Over: Allows the next method call to execute and will pause execution at the next line in the current method.
- Step Into: Step Into steps into the most deeply nested function. For example, if you use Step Into on a call like Func1(Func2()), the debugger steps into the function Func2.
- Step Out: Continues running code and suspends execution when the current function returns. The debugger skips through the current function.
- Restart: 
- Stop: 
- Hot Code Replace: Allows us to modify the source file and push changes to the executing process.
</p>
</details>

#### Remote Debugging

TODO

## Methodology

#### Source vs. Sink

- A 'source' is the code that allows a vulnerability to happen, whereas a 'sink' is where the vulnerability actually happens.
- E.g. when submitting a POST request to login to an application, the controller code that handles this POST request is a source. The code may run some input validation on the username and password and then execute a database query with those values. The call to the database to execute the query is the sink in this scenario.

#### Top down vs. Bottom up

- In a bottom up approach, you start with sinks. Identify if any sinks contain vulnerabilities and what variables/values the vulnerable sink code uses. Then trace the sink and determine which sources call it and what user input can be abused.
- In a top down approach, you start with sources. Trace the application flows to their respective sinks and attempt to identify any sensitive functionality.
- Be mindful of filters and input sanitisation that might affect your payload.
- A bottom up approach is more likely to result in higher-severity vulnerabilities with a lower likelihood of exposure e.g. RCE. A top down approach, however, is likely to uncover lower-severity vulnerabilities with a higher likelihood of exposure e.g. XSS.

## Dangerous Functions

References: 
- Nodejs: https://github.com/rinku191/OSWE-prepration/wiki/Nodejs-Dangerous-function
- C#: https://github.com/rinku191/OSWE-prepration/wiki/C%23-Dangerous-Function
- PHP: https://github.com/rinku191/OSWE-prepration/wiki/PHP-Dangerous-function
- Java: https://github.com/Cryin/JavaID
- Java, Ruby, ASP.NET, PHP, Android: https://github.com/cldrn/InsecureProgrammingDB

## Enable Database Logging

<details><summary>MySQL/MariaDB</summary>
<p>

Modify the following values on my.cnf file (Typically located at /etc/mysql/my.cnf)</br>

```
     [mysqld]
     general_log_file = /var/log/mysql/mariadb.log
     general_log = 1
```
- In case of MariaDB, the settings will be present under `[mariadb]`
- Restart the SQL service for the change to take affect
- You can read the log file in realtime using `sudo tail -f /var/log/mysql/mysql.log`
</p>
</details>

<details><summary>PostgreSQL</summary>
<p>

- https://tableplus.com/blog/2018/10/how-to-show-queries-log-in-postgresql.html
</p>
</details>

## Enable Remote Debugging
- Java: https://stackify.com/java-remote-debugging/
- Java: https://stackoverflow.com/questions/975271/remote-debugging-a-java-application
- Java, PHP, NodeJs: [Requires access to offsec forums] https://forums.offensive-security.com/showthread.php?37965-Visual-Studio-Code-debugging&p=172805

## Possible vulnerabilities that might show up in exam based on the syllabus
|Auth Bypass|RCE|
|---|---|
|SQL Injection - [Payloads](https://portswigger.net/web-security/sql-injection/cheat-sheet)| Deserialization|
|Persistent Cross-Site Scripting	| Bypassing File Upload Restrictions|
IDOR	|SQL Injection RCE (Postgres UDF or Mysql copy to function)|
Weak random token generator	| XXE - [Payloads](https://github.com/payloadbox/xxe-injection-payload-list)|
|Type Juggling	| XML Injection|
|Cross-Site Request Forgery	- [Payloads](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/CSRF%20Injection/README.md#html-get---no-user-interaction)| SSTI - [Payloads](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)|
|Authentication Token/Cookie Manipulation |	Prototype Pollution|
| - |	JavaScript Injection|
| - |	OS Command Injection|

## Vulnerable Code Examples
|Language - PHP|
|---|
|[XSS](/vulnerable-code-examples/php/xss.php)|
|[LFI](/vulnerable-code-examples/php/lfi.php)|
|[SSRF](/vulnerable-code-examples/php/ssrf.php)|
|[OS Command Injection](/vulnerable-code-examples/php/command-injection.php)|
|[SQL Injection - Boolean](/vulnerable-code-examples/php/sql-injection/boolean.php)|
|[SQL Injection - Error](/vulnerable-code-examples/php/sql-injection/error.php)|

## OSWE-like Machines
- https://docs.google.com/spreadsheets/d/1dwSMIAPIam0PuRBkCiDI88pU3yzrqqHkDtBngUHNCw8/edit#gid=665299979

## Skeleton Scripts
|Purpose|File|
|---|---|
|Basic skeleton script which makes an HTTP request in python|[main.py](/skeleton-scripts/main.py)|
| Run shell command and capture the output|[system_level_commands.py](/skeleton-scripts/system_level_commands.py)| 
| Run Java from within Python|[run_java_from_python.py](/skeleton-scripts/run_java_from_python.py)| 
| SQLI multi threaded python exploit|[MYSQL_Injection_multithread.py](/skeleton-scripts/MYSQL_Injection_multithread.py)| 
| Postgres SQLI to RCE JS session riding exploit|[Windows_RCE_XHR.js](/skeleton-scripts/PostgreSQL%20Extensions/Windows/Windows_RCE_XHR.js)| 
| XSS Steal cookie XHR|[steal_cookie_xhr.js](/skeleton-scripts/XSS/steal_cookie_xhr.js)| 
