# Methodology

## Source Code Analysis Checklist

#### 1. Identify the technology stack:

- [x] Programming language? What version, i.e., PHP 5 or 7? Are there programming language-specific vulnerabilities to look out for?
- [x] Database? 
- [x] Framework?
- [x] Templating engine?
- [x] Is it MVC based?
- [x] What are the communication protocols, does it use websockets?
- [x] Does it have an API?
- [x] What Operating System? find ubuntu version using `lsb_release -a`

#### 2. Map the app

- [x] Use `tree -L 3` command, open the app in `VSCode` or build a sitemap using `burp suite` to understand the application directory structure
- [x] What are the routes/pages? If java app search for `doPost` and `doGet`. In case of python find routes starting with `@`
- [x] Is the app MVC based? where are the `Models`, `Views` and `Controllers` located?
    
#### 3. Explore the app

- [x] Is the application running as root?
- [x] Which pages don't require authentication? You can prioritise testing them first
- [x] After checking unauthenticated areas, focus on areas of the application that are likely to receive less attention (i.e. authenticated portions of the application).
- [x] Investigate how sanitization of the user input is performed. Is it done using a trusted, open-source library, or is a custom solution in place?
- [x] MVC: Check if some logic breaks the MVC driven pattern, try to search for direct SQL queries within controller.
- [x] If the application uses a database, how are queries constructed? Does the application parameterize input or simply sanitize it?
- [x] Inspect the logic for account creation or password reset/recovery routines. Can the functionality be subverted?
- [x] Does the application interact with its operating system? If so, can we modify commands or inject new ones?
    
#### 4. Discover vulnerabilities (to bypass authentication)

- [x] What are the interesting functionalities that can be used to bypass authentication? 
    - Password reset component
    - Login component
    - Public comment section or similar
    - Search bar
- [x] SQLi: Find database queries using regex `^.*?query.*?select.*?`
- [x] SSTI: Find templating engine, you might have a similar line `app.set('view engine', 'pug');` in `app.js`
- [x] DOM based XSS: Grep for sinks. REF: https://domgo.at/cxss/sinks 
- [x] Weak random token generator: `java.util.random` is vulnerable

#### 5. Post-Exploitation (post-authentication bypass)

- [x] What are the interesting functionalities that may lead to RCE? 
    - Upload/import functionality
        - Zip jail escape via directory traversal?
