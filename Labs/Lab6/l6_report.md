# **Lab 6 Report**

##### CSCI 5742: Cybersecurity Programming and Analytics, Spring 2026

**Name & Student ID**: [Tejal Jadhav], [111530319]
---

## **Task 1: Implement & Analyze Additional Vulnerabilities**  

1. **Commented Source Code**  
   - *(Paste or attach your commented `vulnerable_program.c` code here. Provide explanations for each vulnerability.)*  

2. **Program Outputs**  
   - *(Insert 3+ screenshots of the program’s output for different inputs — e.g., `./vulnerable_program 1`, `./vulnerable_program 3`, and `./vulnerable_program 5`.)*  

   ![Buffer Overrun Execution](./screenshots/buffer_overrun_execution.png)
   ![Uninitialized Pointer Error](./screenshots/uninitialized_pointer_error.png)
   ![Dangling Pointer Execution](./screenshots/dangling_pointer_execution.png)
   ![Unsafe String Copy Execution](./screenshots/unsafe_string_copy_execution.png)
   ![Buffer Overflow Segmentation Fault](./screenshots/buffer_overflow_segfault.png)
   ![Integer Overflow Result](./screenshots/integer_overflow_result.png)

---

## **Task 2: Out-of-Bounds Write (Valgrind)**
### **Screenshots** 
![Valgrind Version](./screenshots/valgrind_version.png) 
1. *(Screenshot of running `./vulnerable_program 1` without Valgrind.)*
![Run Program Without Valgrind](./screenshots/run_without_valgrind.png)  
2. *(Screenshot of Valgrind output: `valgrind --tool=memcheck ./vulnerable_program 1`.)
![Valgrind Invalid Write Error](./screenshots/valgrind_invalid_write.png)
3. *(Screenshot of Valgrind with `--leak-check=full`.)* 
![Valgrind Full Leak Check](./screenshots/valgrind_full_leak_check.png)
4. *(Screenshot after fixing the `overRun` function to confirm no more errors.)*  
![Valgrind After Fix](./screenshots/valgrind_after_fix.png)

### **Answers to Questions**  
- **1.** Why does this invalid write error happen?  
  This error happens because the program creates space for 10 integers, but then tries to write to x[10]. Since arrays start at index 0, the valid positions are 0 to 9. Writing to index 10 goes outside the allocated memory.

- **2.** Why does Valgrind report an "invalid write of size 4"? What does `4` represent?  
Valgrind reports size 4 because the program is writing 4 bytes of memory.
An integer in C usually takes 4 bytes, so Valgrind shows the size of the memory that was written incorrectly.

- **3.** What is an off-by-one error? Do you see this error in the `overRun` function?  
An off-by-one error happens when a program accesses one element outside the valid range of an array.
Yes, this happens in the overRun function because it tries to access x[10], even though the array only goes from 0 to 9. 

- **4.** What is a memory leak? Explain in your own words. Do you see a memory leak in the `overRun` function?  
A memory leak happens when memory is allocated but never freed. This means the program keeps using memory even when it is not needed anymore. 
Yes, there is a memory leak here because the memory created with malloc() is not freed using free(). 

- **5.** Can errors like this occur in Java? Why or why not?  
Usually no, because Java automatically checks array boundaries. If a program tries to access an invalid index, Java will give an ArrayIndexOutOfBoundsException, so it stops the error from corrupting memory.

- **6.** Compare the Heap Summary from normal Valgrind output vs. `--leak-check=full`. What additional details are shown?  
When running normal Valgrind, it shows the invalid write error and a basic heap summary, like how many bytes were allocated and used.
When using --leak-check=full, Valgrind gives more detailed information about memory leaks. It shows how many bytes are lost, how many blocks are affected, and where the memory was allocated in the code. In this case, it shows that 40 bytes in 1 block are definitely lost, which means the memory allocated with malloc() was not freed.

### **Updated Code for `overRun` Function**  
```c
/* Insert your corrected overRun function here. 
   Include inline comments explaining the fix. */
```
![Fixed overRun Function](./screenshots/fixed_overRun_function.png)

---

## **Task 3: Uninitialized Pointer Analysis**  
### **Screenshots**  
1. *(Screenshot of `valgrind --tool=memcheck --leak-check=full ./vulnerable_program 2`.)
![Valgrind Uninitialized Pointer Error](./screenshots/valgrind_uninitialized_pointer1.png)
![Valgrind Uninitialized Pointer Error](./screenshots/valgrind_uninitialized_pointer2.png)  

2. *(Screenshot with `--track-origins=yes` for more detail.)* 
![Valgrind Track Origins Output](./screenshots/valgrind_track_origins_output1.png)
![Valgrind Track Origins Output](./screenshots/valgrind_track_origins_output2.png)

3. *(Screenshot of fixed function showing no more uninitialized pointer usage issues.)*
![Fixed unInitializedPtr Function](./screenshots/fixed_unInitializedPtr_function.png)
![Valgrind Output After Fix](./screenshots/uninitialized_pointer_fixed.png)

### **Answers to Questions**  
- **7.** Where is the memory problem occurring? What does Valgrind report?  
  The memory problem is happening in the unInitializedPtr function. Valgrind shows the message “Use of uninitialised value of size 8” and also reports errors in functions like strcpy() and strlen().  This indicates that the program is using a pointer that was never initialized, so it contains a random memory address. When functions like strcpy() try to use this pointer, it leads to undefined behavior and memory errors.

- **8.** What is an uninitialized pointer? How could it be exploited?  
  An uninitialized pointer is a pointer that is declared but not assigned any memory address. Because of this, it contains a random value. If the program tries to use it, it may read or write to an unknown memory location. Attackers could exploit this by causing the program to access or overwrite important memory, which could lead to crashes or security vulnerabilities.

- **9.** What is the difference between a `NULL` pointer and an uninitialized pointer?  
  A NULL pointer is a pointer that is intentionally set to NULL, meaning it does not point to any valid memory location. An uninitialized pointer has no value assigned and contains a random memory address. So a NULL pointer is predictable, while an uninitialized pointer can point anywhere in memory.

- **10.** What specifically in the code do you believe caused the uninitialized pointer usage?  
  The issue happens because the pointer is declared but not given a valid memory address before it is used. The program tries to use this pointer in functions like strcpy() or printing functions, which causes the uninitialized memory error.

- **11.** What additional detail does `--track-origins=yes` provide?  
  The `--track-origins=yes` option shows where the uninitialized value was originally created. It traces the problem back to the place in the program where the variable was first used without being initialized. This helps identify the source of the error more clearly.

- **12.** "Use of uninitialized value of size 8" — what does the `8` refer to?  
  The `8` refers to the size of the value being used. On a 64-bit system, a pointer usually takes 8 bytes, so Valgrind reports that an uninitialized value of size 8 is being used.

### **Updated Code for `unInitializedPtr` Function**  
```c
/* Insert your corrected unInitializedPtr function here. 
   Include inline comments explaining the fix. */
```

---

## **Task 4: Dangling Pointer Analysis**  
### **Screenshots**  
1. *(Screenshot of `./vulnerable_program 3` without Valgrind — note behavior.)*  
![Run Program Dangling Pointer](./screenshots/run_dangling_pointer.png)
2. *(Screenshot of Valgrind output: `valgrind --tool=memcheck --leak-check=full --track-origins=yes ./vulnerable_program 3`.)*  
![Valgrind Dangling Pointer Analysis](./screenshots/valgrind_dangling_pointer_analysis.png)
3. *(Screenshot after fixing `danglingPtr`, showing no error.)*  
![Valgrind dangling pointer fixed](./screenshots/valgrind_dangling_pointer_fixed.png)

### **Answers to Questions**  
- **13.** What is the potential issue in the `danglingPtr` function?  
  The issue is that the program frees the memory but still uses the pointer afterward. After free() is called, the pointer still points to that memory location. Accessing it again means the program is using memory that is no longer valid.

- **14.** How could a dangling pointer be exploited?  
  A dangling pointer happens when a pointer still refers to memory that has already been freed. Using this pointer can lead to undefined behavior like incorrect values or crashes. It could be exploited if an attacker replaces that freed memory with other data, causing the program to read or use malicious values.

- **15.** What does Valgrind report about the freed memory usage?  
  Valgrind reports an “Invalid read of size 4”. This means the program is trying to read memory that has already been freed. The pointer still points to the old memory location, so accessing it causes the error.

- **16.** Why does Valgrind possibly show no final "heap error" even though it’s a dangerous bug?  
  Valgrind may show no heap error because the memory was freed correctly, so there is no memory leak. However, the program still tries to access the memory after it was freed, which is dangerous and leads to undefined behavior. 

### **Updated Code for `danglingPtr` Function**  
```c
/* Insert your corrected danglingPtr function here. 
   Include inline comments explaining the fix. */
```
![Fixed danglingPtr function](./screenshots/fixed_danglingPtr_code.png)

---

## **Task 5: Buffer Overflows Analysis**  
### **Screenshots**  
- **For `bufferUnder` (Input 4):**  
  1. *(Screenshot of Valgrind output with `./vulnerable_program 4`.)*  
  ![Valgrind bufferUnder analysis](./screenshots/valgrind_buffer_under.png)
- **For `bufferOver` (Input 5):**  
  2. *(Screenshot of Valgrind output with `./vulnerable_program 5` — if any overflow detected.)* 
  ![Valgrind buffer overflow analysis](./screenshots/valgrind_buffer_overflow.png) 
  3. *(Screenshot of AddressSanitizer detection using `./vulnerable_program2 5`.)*  
  ![AddressSanitizer buffer overflow error](./screenshots/address_sanitizer_overflow1.png)
  ![AddressSanitizer detailed stack overflow report](./screenshots/address_sanitizer_overflow2.png)
  4. *(Screenshot after fixing `bufferOver`, no errors remain.)*  
  ![Program output after fixing buffer overflow](./screenshots/buffer_over_fix_output.png)

### **Answers to Questions**  
- **(Regarding `bufferUnder`, Input 4)**  
  - **15.** Do you see errors in the Valgrind output?  
    No, there are no errors reported by Valgrind. The output shows ERROR SUMMARY: 0 errors and that all heap blocks were freed.

  - **16.** After reading the code, do you expect errors? Why/why not?  
   No, because the buffer size is 256 bytes and the string copied into it does no exceed the buffer size, so it should not cause a buffer overflow. 

- **(Regarding `bufferOver`, Input 5)**  
  - **17.** Do you expect an error here? Why?  
    Yes, an error is expected because the function generates a 260-character string and copies it into a 256-byte buffer using strcpy(). Since the string is larger than the buffer, it can cause a buffer overflow.

  - **18.** Does Valgrind detect it? If so, what is reported?  
    Valgrind does not directly report a buffer overflow, but it reports other memory problems. In the output, Valgrind shows an Invalid free() error and a memory leak of 260 bytes. It also shows ERROR SUMMARY: 2 errors, indicating memory issues caused by the overflow.

  - **19.** Why does Valgrind sometimes struggle to detect this kind of buffer overflow?  
   Valgrind mainly focuses on detecting invalid memory access and heap memory errors. Many buffer overflows occur in stack memory, which Valgrind does not always track precisely. Because of this, it may report indirect errors instead of directly identifying the buffer overflow. 

- **(Valgrind vs. Other Tools)**  
  - **20.** List two additional Valgrind tools besides `memcheck`.  
    Two other tools provided by Valgrind are Helgrind and Massif.

  - **21.** How could these other tools detect errors that `memcheck` misses?  
    Helgrind helps detect problems in multithreaded programs such as race conditions and synchronization errors.
    Massif is a heap profiler that shows how much heap memory a program uses and which parts of the program allocate the most memory. This helps identify memory usage problems that memcheck might not directly highlight. 

### **AddressSanitizer Findings**  
- **22.** What errors does AddressSanitizer report for input `5`?  
  AddressSanitizer reports a stack-buffer-overflow error. It shows that the program writes more data into the buffer than it can hold.

- **23.** Where in the code does it say the error occurs?  
  The error occurs in the bufferOver function where strcpy() copies the large string into the buffer.

- **24.** How does AddressSanitizer compare to Valgrind in detecting buffer overflows?  
  AddressSanitizer detects the buffer overflow more clearly than Valgrind. It directly reports a stack-buffer-overflow error and shows the exact location in the code, while Valgrind only shows indirect memory issues.


### **Updated Code for `bufferOver` Function**  
```c
/* Insert your corrected bufferOver function here. 
   Include inline comments explaining the fix. */
```
![Fixed bufferOver function code](./screenshots/buffer_over_fix_code.png)
---

## **Task 6: Integer Overflow Analysis**  
### **Screenshots**  
1. *(Screenshot of `./vulnerable_program 6` showing normal run — note any incorrect result.)*  
![Integer overflow program output](./screenshots/integer_overflow_normal_run.png)

2. *(Screenshot of `valgrind --tool=memcheck ... ./vulnerable_program 6` showing whether it detects overflow.)*  
![Valgrind integer overflow test](./screenshots/valgrind_integer_overflow.png)

3. *(Screenshot of UBSan detection: `./vulnerable_program2 6`.)*  
![UBSan integer overflow detection](./screenshots/ubsan_integer_overflow.png)

4. *(Screenshot of fixed function, showing no more overflow vulnerability.)*  
![Integer overflow fixed output](./screenshots/integer_overflow_fix_output.png)

### **Answers to Questions**  
- **25.** Why does the overflow occur at `UINT_MAX + 1`?  
  The overflow occurs because INT_MAX is the largest value that a signed integer can store. When 1 is added to this value, it exceeds the limit of the int type and wraps around to a negative number.

- **26.** What are common security risks of integer overflows, and how might attackers exploit them?  
  Integer overflows can cause incorrect calculations or unexpected program behavior. Attackers may exploit this by bypassing security checks, causing crashes, or triggering other vulnerabilities such as buffer overflows.

 - **27.** Does Valgrind report the integer overflow? If not, why?  
 No, Valgrind does not report the integer overflow. The output shows “ERROR SUMMARY: 0 errors”, which means Valgrind did not detect any problem. This happens because Valgrind mainly detects memory-related issues such as invalid memory access or memory leaks. Integer overflow is an arithmetic issue, so it is not detected by Valgrind.

- **28.** Does UBSan report an error?  
  Yes, UBSan reports a runtime error for signed integer overflow. It shows that adding 1 to 2147483647 (INT_MAX) cannot be represented in the int data type.

- **29.** Where in the code does UBSan say the overflow occurs?  
  The overflow occurs in vulnerable_program.c at line 110, inside the integerOverflow function where the addition operation is performed.

- **30.** Compare UBSan’s detection to Valgrind’s.  
  UBSan detects integer overflow more effectively than Valgrind. It directly reports the signed integer overflow and shows the exact line number where it occurs. In contrast, Valgrind mainly detects memory-related issues and does not report integer overflow. 

### **Updated Code for `integerOverflow` Function**  
```c
/* Insert your corrected integerOverflow function here. 
   Include inline comments explaining the fix. */
   ![Fixed integerOverflow function code](./screenshots/integer_overflow_fix_code.png)
```

---

## **Task 7: Static Analysis with Flawfinder**  
### **Screenshots**  
1. *(Screenshot of `flawfinder vulnerable_program.c` output.)*  
![Flawfinder static analysis output](./screenshots/flawfinder_output1.png)
![Flawfinder static analysis output](./screenshots/flawfinder_output2.png)

### **Answers to Questions**  
- **31.** Differentiate static vs. dynamic analysis of source code.  
  Static analysis examines the source code without running the program to find possible security vulnerabilities or coding issues.
  Dynamic analysis tests the program while it is running to detect errors that occur during execution.

- **32.** How do static analysis tools like Flawfinder differ from dynamic tools (Valgrind, AddressSanitizer)?  
Static analysis tools like Flawfinder analyze the code and identify potentially unsafe functions or security weaknesses before the program runs.
Dynamic tools like Valgrind and AddressSanitizer detect problems during program execution, such as memory leaks, buffer overflows, and invalid memory access. 

### **Flawfinder Vulnerabilities**  
- **33.** `strcpy` issues  
  - Location, risk level, CWE classification, and prevention.  
  **Location:** The strcpy function appears in vulnerable_program.c at lines 47, 79, and 92.
  **Risk Level:** Risk level 4 (High Risk).
  **CWE Classification:** CWE-120 – Buffer Copy without Checking Size of Input.
  **Prevention:** Avoid using strcpy because it does not check buffer size. Instead, use safer alternatives such as strncpy, snprintf, or strcpy_s, which limit the number of characters copied and help prevent buffer overflow.

- **34.** `srand` usage (weak randomness)  
  - Why is it a concern, relevant CWE, safer alternatives.  
  .**Why is it a concern:** srand with rand generates predictable pseudo-random numbers, especially when seeded with time(NULL). This makes the random values easier to guess and unsuitable for security-sensitive operations.

  .**Relevant CWE:**CWE-327 – Use of a Broken or Risky Cryptographic Algorithm.

  .**Safer Alternatives:** Use stronger random number generators such as arc4random() or system-based randomness like getrandom() for better unpredictability.

- **35.** Statically-sized arrays  
  - Where used, security risks, relevant CWE, safer approaches.  
  .**Where used:** Statically-sized arrays appear in the code at lines such as 44 and 87, for example: char buffer[256];
  **Security Risks:** If more data is copied into the buffer than its allocated size, it can cause a buffer overflow, potentially leading to memory corruption or program crashes.
  **Relevant CWE:** CWE-121 – Stack-Based Buffer Overflow.
  **Safer Approaches:** Use dynamic memory allocation (e.g., malloc) or implement proper bounds checking before copying data to ensure the buffer size is not exceeded. 

  *(Paste or summarize key parts of the Flawfinder output. Explain any false positives or unaddressed concerns.)*

  Flawfinder found several warnings in the file vulnerable_program.c. The main issues reported were the use of strcpy, srand, statically-sized arrays, and atoi.

  The tool flagged strcpy at line 47, 79, and 92 because strcpy does not check the buffer size when copying data. This can cause a buffer overflow if the input string is larger than the destination buffer.

  Flawfinder also reported srand at line 33. The random numbers generated using rand() may be predictable, which can be a problem if randomness is used for security purposes.

  Another warning was about fixed-size character arrays at lines 44 and 87. If too much data is copied into these buffers, it can overwrite memory and cause errors.

  The tool also flagged atoi at line 119 because it does not validate input properly and may produce unexpected results if the input is invalid.

  Some warnings may be false positives. For example, one strcpy warning says the risk is low because the source string is constant. However, Flawfinder still reports it because strcpy itself is considered unsafe.

  Static analysis tools like Flawfinder show possible problems in the code without running the program, while tools like Valgrind and AddressSanitizer detect issues only during program execution.
---


# **Lab 6: Summary & Reflections**  

### **Key Takeaways from Lab 6**  
*(Summarize your main findings, what you learned, and any challenges faced during the lab.)*  
In this lab, I learned about different types of software vulnerabilities such as buffer overflow, integer overflow, and unsafe memory operations. I used tools like Valgrind, AddressSanitizer, UBSan, and Flawfinder to detect errors and security issues in a C program. Each tool helped identify different types of problems.

One important thing I learned is the difference between dynamic analysis and static analysis. Dynamic tools like Valgrind and AddressSanitizer detect errors when the program is running, while static tools like Flawfinder analyze the source code to find possible vulnerabilities.

I also learned how common C functions like strcpy, atoi, and rand can create security risks if they are not used carefully. Replacing unsafe functions with safer alternatives and adding proper checks can help prevent these issues.

One challenge during the lab was understanding the error messages from the debugging tools and identifying where the problem was in the code. However, by analyzing the outputs and checking the source code, I was able to locate the vulnerabilities and fix them. Overall, this lab helped me understand how important secure coding practices and debugging tools are in preventing software vulnerabilities.
