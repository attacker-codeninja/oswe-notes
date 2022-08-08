# My OSWE Journey

Time for OSWE I guess.

* **07/08/2022**: Journey begins

# Fundamentals

## Tools

#### General

- [x] [CyberChef](https://gchq.github.io/CyberChef/) A web app for encryption, encoding, compression and data analysis
- [x] [JSNICE](http://jsnice.org/) A JavaScript Deobfuscation tool
- [x] [boxentriq/code-breaking](https://www.boxentriq.com/code-breaking) Various codebreaking and cipher tools

#### Decompilers

- [x] [dnSPY](https://github.com/dnSpy/dnSpy) - .NET decompiler
- [x] [JD-GUI](http://java-decompiler.github.io/) - Java decompiler

## Source Code Review Methdologies
S. No| Approach|
|     :---:      |     :---:      |
|1|String matching/Grep for bugs |
|2|Following user input|
|3|Reading source code randomly|
|4|Read all the code|
|5|Check one functionality at a time (login, password reset...)|

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

## OSWE: Possible vulnerabilities that might show up in exam based on the syllabus
|Auth Bypass	| RCE|
|     :---:      |     :---:      |
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
| Language - PHP|
|     :---:      |
|[XSS](/Vulnerable%20Code%20Examples/php/xss.php)|
|[LFI](/Vulnerable%20Code%20Examples/php/lfi.php)|
|[SSRF](/Vulnerable%20Code%20Examples/php/ssrf.php)|
|[OS Command Injection](/Vulnerable%20Code%20Examples/php/commandInjection.php)|
|[SQL Injection - Boolean](/Vulnerable%20Code%20Examples/php/sqlinjection/boolen.php)|
|[SQL Injection - Error](/Vulnerable%20Code%20Examples/php/sqlinjection/error.php)|

## Code Review Checklist
- [x] Identify Tech Stack: 
    - [x] Programming language? What version, i.e., PHP 5 or 7? 
    - [x] Database? 
    - [x] Framework?
    - [x] Templating engine?
    - [x] Is it MVC based?
    - [x] What are the communication protocols, does it use websockets?
    - [x] Does it have an API?
    - [x] What Opertating System? find ubuntu version using lsb_release -a
- [x] Map the app
    - [x] Use `tree -L 3` command, open the app in `VSCode` or build a sitemap using `burp suite` to understand the application directory structure
    - [x] What are the routes/pages? If java app search for `doPost` and `doGet`. In case of python find routes starting with `@`
    - [x] Is the app MVC based? where are the `Models`, `Views` and `Controllers` located?
- [x] Explore the app
    - [x] Is the application running as root?
    - [x] Which pages don't require authentication? You can prioritise testing them first
    - [x] MVC: Check if some logic breaks the MVC driven pattern, try to search for direct SQL queries within controller
- [x] Discover vulnerabilities
    - [x] What are the interesting functionalities? Password reset, comment section visible to all users, search bar etc
    - [x] SQLi: Find database queries using regex `^.*?query.*?select.*?`
    - [x] SSTI: Find templating engine, you might have a similar line `app.set('view engine', 'pug');` in `app.js`
    - [x] DOM based XSS: Grep for sinks. REF: https://domgo.at/cxss/sinks 
    - [x] Weak random token generator: `java.util.random` is vulnerable

## OSWE Like Machines
- https://www.vulnhub.com/entry/securecode-1,651/
- https://github.com/bmdyy

## Skeleton Scripts
|Purpose	| File|
|     :---:      |     :---:      |
|Basic skeleton script which makes an HTTP request in python|[main.py](/Skeleton%20Scripts/main.py)|
| Run shell command and capture the output|[system_level_commands.py](/Skeleton%20Scripts/system_level_commands.py)| 
| Run Java from within Python|[run_java_from_python.py](/Skeleton%20Scripts/run_java_from_python.py)| 
| SQLI multi threaded python exploit|[MYSQL_Injection_multithread.py](/Skeleton%20Scripts/MYSQL_Injection_multithread.py)| 
| Postgres SQLI to RCE JS session riding exploit|[Windows_RCE_XHR.js](/Skeleton%20Scripts/PostgreSQL%20Extension/Windows/Windows_RCE_XHR.js)| 
| XSS Steal cookie XHR|[steal_cookie_xhr.js](/Skeleton%20Scripts/XSS/steal_cookie_xhr.js)| 
