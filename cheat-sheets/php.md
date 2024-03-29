# PHP

## Tips

### Disclosing the Web Root

A typical method is abuse of the `display_errors` PHP setting. Leverage the `display_errors` misconfiguration is by sending a GET request with arrays injected as parameters, if the back-end code does not expect arrays as input data a warning error can be triggered.

`GET /ATutor/browse.php?access=&search[]=test&include=all&filter=Filter HTTP/1.1`

## Type Juggling

Types:
- "string" for strings
- int(0), float(0) for numbers
- TRUE, FALSE for booleans

Terms:
- "Zero-like" - an expression that PHP will loosely compare to int(0)

Background:
- PHP Has two main comparison modes, lets call them **loose** (`==`) and **strict** (`===`)
- Loose comparisons have a set of operand conversion rules to make it easier for developers
- Some of them are a bit weird
- Type juggling oddities have been improved in PHP 7 and again in PHP 8, these types of problems are more common in <= PHP 5

> PHP8 won't try to cast string into numbers anymore, thanks to the Saner string to number comparisons RFC, meaning that collision with hashes starting with 0e and the likes are finally a thing of the past! The Consistent type errors for internal functions RFC will prevent things like `0 == strcmp($_GET['username'], $password)` bypasses, since strcmp won't return null and spit a warning any longer, but will throw a proper exception instead. 

#### True statements

```php
var_dump('0010e2'   == '1e3');           # true
var_dump('0xABCdef' == ' 0xABCdef');     # true PHP 5.0 / false PHP 7.0
var_dump('0xABCdef' == '     0xABCdef'); # true PHP 5.0 / false PHP 7.0
var_dump('0x01'     == 1)                # true PHP 5.0 / false PHP 7.0

var_dump('0xAAAA'   == '43690');           # true PHP 5.0 / false PHP 7.0
var_dump('0xAAAA'   == 43690);             # true PHP 5.0 / false PHP 7.0
var_dump(0xAAAA     == 43690);             # true PHP 5.0 / true PHP 7.0
var_dump('0xAAAA'   == '43691');           # false PHP 5.0 / false PHP 7.0
```

```php
'123'  == 123
'123a' == 123
'abc'  == 0
```

```php
'' == 0 == false == NULL
'' == 0       # true
0  == false   # true
false == NULL # true
NULL == ''    # true
```

#### NULL statements

```php
var_dump(sha1([])); # NULL
var_dump(md5([]));  # NULL
```

#### Magic Hashes - Exploit

If the hash computed starts with "0e" (or "0..0e") only followed by numbers, PHP will treat the hash as a float.

| Hash | “Magic” Number / String    | Magic Hash                                    |
| ---- | -------------------------- |:---------------------------------------------:|
| MD5  | 240610708                  | 0e462097431906509019562988736854              |
| MD5  | QNKCDZO                    | 0e830400451993494058024219903391              |
| MD5  | 0e1137126905               | 0e291659922323405260514745084877              |
| MD5  | 0e215962017                | 0e291242476940776845150308577824              |
| MD5  | 129581926211651571912466741651878684928                | 06da5430449f8f6f23dfc1276f722738              |
| SHA1 | 10932435112                | 0e07766915004133176347055865026311692244      |
| SHA-224 | 10885164793773          | 0e281250946775200129471613219196999537878926740638594636 |
| SHA-256 | 34250003024812          | 0e46289032038065916139621039085883773413820991920706299695051332 |
| SHA-256 | TyNOQHUS                | 0e66298694359207596086558843543959518835691168370379069085300385 |

```php
<?php
var_dump(md5('240610708') == md5('QNKCDZO')); # bool(true)
var_dump(md5('aabg7XSs')  == md5('aabC9RqS'));
var_dump(sha1('aaroZmOk') == sha1('aaK1STfY'));
var_dump(sha1('aaO8zKZF') == sha1('aa3OFF9m'));
?>
```

#### PHP Comparisons: Strict

![Strict Comparison Chart](https://raw.githubusercontent.com/tkashro/oswe-notes/master/img/php-strict-comparisons.png)

#### PHP Comparisons: Loose

![Loose Comparison Chart](https://raw.githubusercontent.com/tkashro/oswe-notes/master/img/php-loose-comparisons.png)

#### The Logic

When a string is evaluated in a numeric context, the resulting value and type are determined as follows:
- If the string does not contain any of the characters `.`, `e`, or `E` and the numeric value fits into integer type limits (as defined by `PHP_INT_MAX`), the string will be evaluated as an integer. In all other cases it will be evaluated as a float.
- The value is given by the initial portion of the string. If the string starts with valid numeric data, this will be the value used. Otherwise, the value will be 0 (zero). 
- Valid numeric data is an optional sign, followed by one or more digits (optionally containing a decimal point), followed by an optional exponent. The exponent is an `e` or `E` followed by one or more digits.

When loose comparing a **string to a number**, PHP will attempt to convert the string to a number then perform a numeric comparison:

> Note: PHP 7 will only cast strings to numeric data where the string is considered valid numeric data. PHP 5 is looser and does not require valid numeric data.
> Hexadecimal strings are no longer considered numeric in PHP 7 (https://www.php.net/manual/en/migration70.incompatible.php#migration70.incompatible.strings).

```
TRUE: "0000" == int(0)    # true PHP 5.0 / true PHP 7.0
TRUE: "0e12" == int(0)    # true PHP 5.0 / true PHP 7.0
TRUE: "1abc" == int(1)    # true PHP 5.0 / false PHP 7.0
TRUE: "0abc" == int(0)    # true PHP 5.0 / false PHP 7.0
TRUE: "abc" == int(0)     // !!
```

If PHP decides that both operands look like numbers, even if they are actually strings, it will convert them both and perform a numeric comparison:
```
TRUE: "0e12345" == "0e54321"
TRUE: "0e12345" <= "1"
TRUE: "0e12345" == "0"
TRUE: "0xF" == "15"
```

> Note: Interpretation rules for exponent notations have not changed in PHP 7

```
var_dump('0eAAAA' == '0'); # false PHP 5.0 / false PHP 7.0 - Not valid numeric data as per logic rules outlined above, therefore no string to number conversion is performed
var_dump('0e1111' == '0'); # true PHP 5.0 / true PHP 7.0
var_dump('0e9999' == 0);   # true PHP 5.0 / true PHP 7.0
```

## Dangerous PHP Functions

### Acquiring User Supplied Input
```
$_GET and $HTTP_GET_VARS          // parameter submitted in query string Ex: $_GET['username']
$_POST and $HTTP_POST_VARS        // parameter submitted in request body string Ex: $_POST['username']
$_COOKIE and $HTTP_COOKIE_VARS    // cookies submitted in the request Ex: $_COOKIE['name']
$_REQUEST                         // contains all item the item in $_GET, $_POST and $_COOKIE
$_FILES and $HTTP_POST_FILES      // contains file uploaded in the request
$_SERVER['PHP_SELF']              // contains current executing page
$_SESSION                         // store session value Ex: $_SESSION['username'] = $_POST['username']
```

### Command Execution
```
exec           - Returns last line of commands output
passthru       - Passes commands output directly to the browser
system         - Passes commands output directly to the browser and returns last line
shell_exec     - Returns commands output
\`\` (backticks) - Same as shell_exec()
popen          - Opens read or write pipe to process of a command
proc_open      - Similar to popen() but greater degree of control
pcntl_exec     - Executes a program
```

### PHP Code Execution
#### Apart from eval there are other ways to execute PHP code: include/require can be used for remote code execution in the form of Local File Include and Remote File Include vulnerabilities.

```eval()
assert()  - identical to eval()
preg_replace('/.*/e',...) - /e does an eval() on the match
create_function()
include()
include_once()
require()
require_once()
$_GET['func_name']($_GET['argument']);
$func = new ReflectionFunction($_GET['func_name']); $func->invoke(); or $func->invokeArgs(array());
```



### List of functions which accept callbacks
#### These functions accept a string parameter which could be used to call a function of the attacker's choice. Depending on the function the attacker may or may not have the ability to pass a parameter. In that case an Information Disclosure function like phpinfo() could be used.
```
Function                     => Position of callback arguments
'ob_start'                   =>  0,
'array_diff_uassoc'          => -1,
'array_diff_ukey'            => -1,
'array_filter'               =>  1,
'array_intersect_uassoc'     => -1,
'array_intersect_ukey'       => -1,
'array_map'                  =>  0,
'array_reduce'               =>  1,
'array_udiff_assoc'          => -1,
'array_udiff_uassoc'         => array(-1, -2),
'array_udiff'                => -1,
'array_uintersect_assoc'     => -1,
'array_uintersect_uassoc'    => array(-1, -2),
'array_uintersect'           => -1,
'array_walk_recursive'       =>  1,
'array_walk'                 =>  1,
'assert_options'             =>  1,
'uasort'                     =>  1,
'uksort'                     =>  1,
'usort'                      =>  1,
'preg_replace_callback'      =>  1,
'spl_autoload_register'      =>  0,
'iterator_apply'             =>  1,
'call_user_func'             =>  0,
'call_user_func_array'       =>  0,
'register_shutdown_function' =>  0,
'register_tick_function'     =>  0,
'set_error_handler'          =>  0,
'set_exception_handler'      =>  0,
'session_set_save_handler'   => array(0, 1, 2, 3, 4, 5),
'sqlite_create_aggregate'    => array(2, 3),
'sqlite_create_function'     =>  2,
```

### Information Disclosure
#### Most of these function calls are not sinks. But rather it maybe a vulnerability if any of the data returned is viewable to an attacker. If an attacker can see phpinfo() it is definitely a vulnerability.
```
phpinfo
posix_mkfifo
posix_getlogin
posix_ttyname
getenv
get_current_user
proc_get_status
get_cfg_var
disk_free_space
disk_total_space
diskfreespace
getcwd
getlastmo
getmygid
getmyinode
getmypid
getmyuid
```

### Other
```
extract - Opens the door for register_globals attacks (see study in scarlet).
parse_str -  works like extract if only one argument is given.  
putenv
ini_set
mail - has CRLF injection in the 3rd parameter, opens the door for spam. 
header - on old systems CRLF injection could be used for xss or other purposes, now it is still a problem if they do a header("location: ..."); and they do not die();. The script keeps executing after a call to header(), and will still print output normally. This is nasty if you are trying to protect an administrative area. 
proc_nice
proc_terminate
proc_close
pfsockopen
fsockopen
apache_child_terminate
posix_kill
posix_mkfifo
posix_setpgid
posix_setsid
posix_setuid
```

### Filesystem Functions
#### According to RATS all filesystem functions in php are nasty. Some of these don't seem very useful to the attacker. Others are more useful than you might think. For instance if allow_url_fopen=On then a url can be used as a file path, so a call to copy($_GET['s'], $_GET['d']); can be used to upload a PHP script anywhere on the system. Also if a site is vulnerable to a request send via GET everyone of those file system functions can be abused to channel and attack to another host through your server.

```
// open filesystem handler
fopen
tmpfile
bzopen
gzopen
SplFileObject->__construct
// write to filesystem (partially in combination with reading)
chgrp
chmod
chown
copy
file_put_contents
lchgrp
lchown
link
mkdir
move_uploaded_file
rename
rmdir
symlink
tempnam
touch
unlink
imagepng   - 2nd parameter is a path.
imagewbmp  - 2nd parameter is a path. 
image2wbmp - 2nd parameter is a path. 
imagejpeg  - 2nd parameter is a path.
imagexbm   - 2nd parameter is a path.
imagegif   - 2nd parameter is a path.
imagegd    - 2nd parameter is a path.
imagegd2   - 2nd parameter is a path.
iptcembed
ftp_get
ftp_nb_get
// read from filesystem
file_exists
file_get_contents
file
fileatime
filectime
filegroup
fileinode
filemtime
fileowner
fileperms
filesize
filetype
glob
is_dir
is_executable
is_file
is_link
is_readable
is_uploaded_file
is_writable
is_writeable
linkinfo
lstat
parse_ini_file
pathinfo
readfile
readlink
realpath
stat
gzfile
readgzfile
getimagesize
imagecreatefromgif
imagecreatefromjpeg
imagecreatefrompng
imagecreatefromwbmp
imagecreatefromxbm
imagecreatefromxpm
ftp_put
ftp_nb_put
exif_read_data
read_exif_data
exif_thumbnail
exif_imagetype
hash_file
hash_hmac_file
hash_update_file
md5_file
sha1_file
highlight_file
show_source
php_strip_whitespace
get_meta_tags
```
