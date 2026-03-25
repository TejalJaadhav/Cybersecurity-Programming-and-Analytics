# **Lab 5 Report**

##### CSCI 5742: Cybersecurity Programming and Analytics, Spring 2026

**Name & Student ID**: [Tejal Jadhav], [111530319]

---

# **Part 1: Reconnaissance & Web Scanning (10 pts + 2 bonus pts)**

## **Task 1: Discover Web Services (5 pts)**

#### **Screenshot:**

![Open Web Ports](./screenshots/open_web_ports.png)
![DVWA](./screenshots/dvwa.png)
![Mutillidae](./screenshots/mutillidae.png)
![Tomcat Manager](./screenshots/tomcat_manager.png)


#### **Answers to Questions:**

1. Which ports are hosting web services?
The Nmap scan shows that port 80 and port 8180 are open on the Metasploitable 2 system. These ports are hosting web services.

2. What web applications are running?
The system is running several vulnerable web applications. DVWA (Damn Vulnerable Web Application) and Mutillidae are accessible through the web server on port 80. The Apache Tomcat Manager application is running on port 8180.

---

## **Task 2: Web Directory Enumeration (5 pts)**

#### **Screenshots:**

![Web Directories with dirb](./screenshots/web_directory_with_dirb1.png)
![Web Directories with dirb](./screenshots/web_directory_with_dirb2.png)
![Web Directories with dirb](./screenshots/web_directory_with_dirb3.png)
![Web Directories with dvwa](./screenshots/web_directory_with_dirb_dvwa1.png)
![Web Directories with dvwa](./screenshots/web_directory_with_dirb_dvwa2.png)
![Web Directories with mutillidae](./screenshots/web_directory_with_dirb_mutillida1.png)
![Web Directories with mutillidae](./screenshots/web_directory_with_dirb_mutillida2.png)
![Scan for File Extension](./screenshots/scan_for_file_extension.png)

#### **Answers to Questions:**

3. List three important directories found by `dirb`.
Three important directories discovered during the scan are /phpMyAdmin, /dvwa/config, and /mutillidae/includes. These directories are important because they may contain configuration files, database management interfaces, or application code that could expose sensitive information.

4. Why is directory enumeration useful for web attacks?
Directory enumeration helps attackers discover hidden directories, login pages, configuration files, and admin panels that are not directly linked on the website. Finding these locations can reveal sensitive information or vulnerable files that can be exploited to gain unauthorized access to the web application or server.

---

## **Task 3: Identify Technologies Used by the Web Apps (Bonus Exploration, 2 pts)**

#### **Screenshot:**
![WhatWeb](./screenshots/whatweb.png)

#### **Answer to Question:**

5. How could knowing the technology stack help an attacker?
Knowing the technology stack helps an attacker understand what software the web server is using, such as Apache, PHP, and WebDAV. If these technologies are outdated or have known vulnerabilities, the attacker can search for existing exploits for those versions and try to use them to attack the system. This makes it easier to find weaknesses and plan an attack.

---
## **Task 4: Web Server Vulnerability & Misconfiguration Scan with Nikto**

#### **Screenshot:**


![Nikto](./screenshots/nikto.png)
![Nikto with Output File](./screenshots/nikto_with_output_file.png)


#### **Answer to Questions:**

6. List two findings Nikto reported.
Nikto showed that the Apache server version 2.2.8 is running, which is an old version. It also found that the phpinfo.php page is accessible, which displays detailed information about the PHP configuration of the server.


7. For one finding, explain how it could be leveraged in a real attack scenario (high level).
If the phpinfo.php page is accessible, it shows a lot of system details like the PHP version, installed modules, and server configuration. An attacker could use this information to understand the server setup and then look for known vulnerabilities related to that PHP version or configuration.


---

# **Part 2: SQL Injection (SQLi) (30 pts + 3 bonus pts)**

## **Task 1: Manually Exploit SQL Injection in DVWA (15 pts)**

#### **Screenshots:**

 ![dvwa with Low Security](./screenshots/dvwa_with_low_security.png)
 ![SQL Injection Payload with User ID](./screenshots/sql_injection_payload_user_id.png)
 ![SQL Injection Payload with Union](./screenshots/sql_injection_payload_union.png)



#### **Answers to Questions:**

8. What happens when you submit this input?
When the input ' OR '1'='1' # is submitted, the application returns all user records from the database. Instead of showing only one user based on the ID, the page displays multiple users such as admin, Gordon, Pablo, and others. This happens because the condition '1'='1' is always true, so the query returns every record.

9. Why does the server return valid results?
The server returns valid results because the application does not properly validate or filter the input before sending it to the database. The injected SQL code becomes part of the database query, and since the condition is always true, the database executes the query and returns all matching records.

---

## **Task 2: Automate SQL Injection with SQLmap (15 pts)**

#### **Screenshots:**

![Captured PHPSESSID from Developer Tools](./screenshots/php_session_cookie.png)
![SQLMap Detects SQL Injection and Lists Databases](./screenshots/sqlmap_detects_sqli_and_databases1.png)
![SQLMap Detects SQL Injection and Lists Databases](./screenshots/sqlmap_detects_sqli_and_databases2.png)
![SQLMap Detects SQL Injection and Lists Databases](./screenshots/sqlmap_detects_sqli_and_databases3.png)
![SQLMap Detects SQL Injection and Lists Databases](./screenshots/sqlmap_detects_sqli_and_databases4.png)
![SQLMap Detects SQL Injection and Lists Databases](./screenshots/sqlmap_detects_sqli_and_databases5.png)

![SQLMap Listing Tables in dvwa Database](./screenshots/sqlmap_dvwa_tables1.png)
![SQLMap Listing Tables in dvwa Database](./screenshots/sqlmap_dvwa_tables2.png)

![SQLMap - Dump users table](./screenshots/sqlmap_dvwa_users_dump1.png)
![SQLMap - Dump users table](./screenshots/sqlmap_dvwa_users_dump2.png)

![Locate users.csv](./screenshots/users_csv_location.png)

![Extracted hashes to hashes.txt](./screenshots/extract_hashes_txt.png)

#### **Answers to Questions:**

10. What databases exist on the server?
The database discovered on the server was dvwa (Damn Vulnerable Web Application database). This database contains tables such as users and guestbook, which store application data including user credentials.

11. How can an attacker use dumped credentials to escalate an attack?
An attacker can use the dumped credentials to log into user accounts in the application. If any of the credentials belong to an admin account or are reused on other services (like SSH or databases), the attacker could gain higher privileges or access to other systems, which helps them continue the attack.

---

## **Bonus: Crack the Password Hashes (3 pts)**

#### **Screenshots:**



![Hash identification using hashid](./screenshots/hashid_hash_type.png)
![John the Ripper cracked passwords](./screenshots/john_cracked_passwords.png)

*(Optional notes: briefly mention which hashes were cracked and what they cracked to.)*
The hashes were identified as MD5 and cracked using John the Ripper with the RockYou wordlist. The passwords recovered were: password, abc123, letmein, and charley.

---

# **Part 3: Cross-Site Scripting (XSS) (30 pts)**

## **Task 1: Exploit Reflected XSS (10 pts)**

#### **Screenshots:**


![Reflected XSS alert popup](./screenshots/reflected_xss_alert.png)
![Captured cookie using Netcat](./screenshots/xss_cookie_capture.png)

---

## **Task 2: Exploit Stored XSS (10 pts)**

#### **Screenshots:**


![Stored XSS Alert](./screenshots/stored_xss_alert.png)
![Stored XSS Source](./screenshots/stored_xss_source.png)

---

## **Task 3: Advanced Stored XSS: Multi-Step Cookie Theft (10 pts)**

#### **Screenshots:**

![Stored XSS Payload Step 1](./screenshots/xss_payload_step1.png)
![Stored XSS Payload Step 2](./screenshots/xss_payload_step2.png)
![Stored XSS Payload Step 3](./screenshots/xss_payload_step3.png)
![Stolen Cookie Captured in Netcat](./screenshots/xss_cookie_capture_netcat.png)

---

# **Part 4: Directory Traversal (Local File Inclusion - LFI) (15 pts)**

## **Task 1: Exploit Local File Inclusion (LFI) (15 pts)**

#### **Screenshot:**

![LFI attack displaying /etc/passwd](./screenshots/lfi_etc_passwd.png)

#### **Answer to Question:**

12. What did you find in `/etc/passwd`?
The /etc/passwd file shows the list of users on the Linux system. It contains information like usernames, user IDs, group IDs, home directories, and login shells. In the file I could see accounts such as root, daemon, www-data, mysql, and postgres. This means the LFI vulnerability allowed access to a sensitive system file.

---

# **Part 5: Cross-Site Request Forgery (CSRF) (15 pts)**

## **Task 1: Perform a Basic CSRF Attack Using a Simple Link (15 pts)**

#### **Screenshots:**

![CSRF attack successfully changing password](./screenshots/csrf_password_changed.png)
![CSRF attack success](./screenshots/csrf_attack_success1.png)
![CSRF attack success](./screenshots/csrf_attack_success2.png)

#### **Answers to Questions:**

13. Why is a GET request for password changes insecure?
GET requests are not secure for password changes because the data is sent in the URL. Anyone can see or modify the URL parameters. If a user clicks on a malicious link while logged in, the request can run automatically and change the password without the user realizing it.

14. How does this attack work without JavaScript?
This attack works without JavaScript because it only uses a normal HTML link. When the victim clicks the link, the browser sends the request to the server automatically. Since the victim is already logged in, the browser includes the session information and the server accepts the request.

15. How could DVWA prevent this attack?
DVWA could prevent this attack by using CSRF tokens. A CSRF token is a unique value added to forms that the server checks before accepting the request. Another way is to use POST requests for sensitive actions like password changes and verify where the request is coming from.

