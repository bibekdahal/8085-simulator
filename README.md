# 8085 + 8255 Simulatior

Main Application: Emulator.py

## Documentation
### Problem Statement

As part of the subject course of Instrumentation II, the project **8085 Microprocessor and 8255 PPI Simulator** has been assigned to us. In the project, we were assigned to design a software simulating the 8085 Microprocessor and the 8255 PPI and write the software in Python language. The objective of such project was for us to familiarize in emulating an instrumentation system in software.
Additionally, we were assigned to write a program in assembly language that can:
- generate 100 random numbers in range from 00H to FFH, without repeatition
- store the random numbers in memory
- sort the random numbers in ascending order using selection sort and in descending order using bubble sort
- take the type of sorting as input from push buttons on 8255 PPI

### Design Approach

The software is built in Python scripting language using Object Oriented approach. Classes representing different elements of the microprocessor and the PPI are created with appropriate methods. 

The software is built using sequential design process. After understanding the problem statement, appropriate tools for developement were chosen and the overall project was designed in paper. The 8085 and 8255 were then developed and tested to run by reading machine langauge program from a text file. Then an assembler to read assembly language program and convert it to machine codes was built. Finally a graphical user interface (GUI) was added for proper user interaction. Finally, the random data sorter program was written ans successfully tested in the developed software.

For efficient teamwork and version control, GIT version control system is used. The central repository of the program is hosted in GitHub.

##### 8085 Microprocessor and 8255 PPI
The 8085 and 8255 were designed using combinations of objects of following classes:
###### ALU
The Arithmetic Logic Unit is emulated using a class containing an array of registers (each storing a byte) and the methods to perform various arithmetic and logical operations like Add, Subtract, And, Or, Xor, Not etc. As with 8085, the ALU assumes one of its operand as register 'A' and can take any other byte as its second operand. For Double Addition, it assumes one of its operand as HL-register pair and can take any other double-bytes as second operand. The register array holds the general purpose registers (A, B, C, D, E, H, L), the flags (F), the program counter (PC) and the stack pointer (SP).
###### CU
The Control Unit is represented using a class that hold a reference to an ALU and a Bus. It has methods to fetch, decode and execute instruction from any memory address. It can read byte from memory as addressed by the program counter (Fetch), check the byte to find out the operation to be performed (Decode) and perform the operation specified (Execute). While executing, it can fetch further instruction bytes if needed. The memory read-write and IO read-write operations are performed through the Bus. The registers of ALU are directly or indirectly used by the CU, including reading/writing to the general puspose registers, using ALU to perform operations on them, incrementing/changing program counter's value and using/modifying the stack pointer's value. Interrupts got at middle of any operation is stored and only acknowledged and handled at end of each Fetch-Decode-Execute cyle.
###### Bus
It is used to address map the peripheral and memory devices using IO-mapping or memory-mapping scheme. Any device can be assigned a range of memory or IO addresses. The CU can then use the Bus to read/write data and the Bus will further use the appropriate device object to handle such data.
###### RAM
RAM holds an array of bytes of size specified (by default 64K). Each byte can be read and written to using valid address. The memory bytes are accessed through the Bus.
###### PPI
The 8255 PPI can be addressed as IO or memory using the Bus. The PPI stores 4 bytes in Port-A, Port-B, Port-C and Control Register. The read/write operation (performed by CU through the Bus) are handled according to the control word held in the control register. For Mode-1 and Mode-2 input operations, interrupt function objects can be assigned to the PPI, so that when strobe signal is sent, the interrupt function is called. The actual interrupt functions are implemented in the CU.

The relation between above classes is shown in following UML diagram.

![](images/UML.jpeg?raw=true)

Following design patterns were used in designing above elements:
###### Signal Line Representation
Interrupt and Interrupt Acknowledge signals, IO/Memory addresses and data and any other signals that can flow through hardware wires/lines are implemented using simple function calls. Any data to be placed is sent as parameter to such function. For example, when the PPI needs to send the interrupt signal to the microprocessor, it calls the Interrupt function of the CU and the microprocessor to acknowledge the interrupt calls the Interrupt-Acknowledge function of the interrupting object.
###### Byte Storage
Since Python doesn't have specific "byte" data type, just number is stored when storing a byte. Appropriate checkings are done at proper positions in the program to allow only bytes.
###### Asynchronous Interrupts
Interrupts can be provided at the middle of operations. To allow this asynchronous behaviour, multithreading is used. The CU executes the operations in a different thread and the devices can provide interrupts from the main thread.
###### Machine Codes
Since the machine language opcodes are too many, proper analysis to find a common pattern among the opcodes is used to simplify the programming of the CU.

##### Assembler
The Assembler is built using a single class that can read from a file any assembly or machine langauge program and convert them into each other. Process of parsing contains simple steps of:
- lexically analyzing the tokens and store the tokens in list
- syntatically analyzing the list of tokens to find errors
- converting the syntatically analyzed tokens from assembly language to machine language (or vice versa)

The overall assembling process is explained in following flowchart.
![](images/Assembler-Flow-Chart.jpg?raw=true)

##### GUI
The GUI is built using GTK library for Python (PyGObject). The library was chosen to make the software cross platform. The GUI consists of interfaces for both 8085 and 8255. The 8085 GUI consists of buttons and displays similar to the kit in the college laboratory and can be used to input program and data to memory, to view register values, to perform single step execution and to run the program from certain memory address. Besides these, it also contains a text editor with syntax highlighting features for writing and viewing assembly programs. The program from the editor can be assembled and loaded to the memory at any given address and can be run instantly. The 8255 GUI contains options to provide inputs to the ports, read outputs from the ports and strobe buttons (S1 and S2) for strobed input.

For the GUI emulating the Kit buttons, a kind of state machine is implemented. This allows the UI to remember the last buttons pressed and act accordingly when another button is pressed. The basis of this state machine is illustrated in following simple state diagram.
![](images/8085GUIStateDiagram.jpg?raw=true)

##### Random Data Generator and Data Sorter:
For random data generation, a simple version of XOR-Shift algorithm is used. A seed value X is taken and bit shifted once to left. The bit-shifted X and the original X are xor-ed together to get a new random value. This random value acts as seed value for next generation.
For data sorting, selection sort and bubble sort are both implemented. These functions are then appropriately called as per the user input from PPI.

###### Random Data Generator Alogrithm
1. Take seed value X
2. Left-shift X once: LSH(X)
3. XOR the original X and LSH(X) to get new X: X = X xor LSH(X)
4. Return X as random value and store it as new seed value for next generation

###### Selection Sort Algorithm for sorting in ascending order
* For j = 0 to N-2
    * imin = j
    * For i = j to n-1
        * If a[i] < a[imin]
        *     imin = i
    * If imin != j
        * Swap(a[j], a[imin])

###### Bubble Sort Algorithm for sorting in descending order
* Repeat until not swapped
    * swapped = False
    * For i = 1 to n-1
        * If a[i-1] < a[i]
            * Swap(A[i-1], A[i])
            * swapped = True

### Source Code

TODO

### GUI Results

![Main Window](images/GUI0.png?raw=true)


![PPI Window](images/PPI0.png?raw=true)
TODO: Snapshots

### Comparision of simulation output and hardware output

##### Review of Assembly Language Programming (Lab 1)
All programs were successfully run in both hardware and simulator and gave exactly same result.

##### Interfacing with 8255 PPI (Lab 2)
While the 8255 PPI hardware and PPI window of simulator were feature-wise slightly different, the actual output from programs run in both were similar and the simulator can be considered to be good substitute for actual hardware.

##### Data Sorter
The final output of data sorter from both hardware and simulator were same. However, the time required by the simulator seems longer in both random generation and data sorting process.

### Discussion and Analysis
The final result of the program is obtained as was designed and expected. Following features have been successfully implemented:
- Simulation of 8085 microprocessor and 8255 PPI
- GUI emulating the behaviour of 8085 microprocessor lab kit
- Code Editor with syntax highlighting for writing, loading and saving assembly language programs
- Assembler to assemble the assembly language programs and view syntax errors in a program
- Attach any number of 8255 PPIs at any IO addresses
- Input to ports of 8255 PPI, view output from the ports and send STB singnals to PPI using buttons
- View table of memory data

Final program simulates the behaviour of 8085 and 8255 well in functionality. However the timing behaviour was not quite the best. The random number generation and data sorting algorithms take longer than expected. This is mainly due to python being a scripting language and simulator being run by software rather than hardware. Another limitation of the simulator is lack of peripherals. While the design of software is extensible to accept further hardware-simulating programs, the acutal final software only supports RAM and PPI. Yet any 8085 program can be run by the simulator that requires memory and 8255 PPI only as peripherals.

### Conclusion

The software development was successfully completed in time. This is probably due to good design and problem planning at the beginning. Chances to learn new programming language and libraries was obtained through this project and we are very glad to participate in it.

This software itself can be considered successful in terms of its functionality. Hopefully, it can help students in learning the programing of 8085 and 8255 hardwares without availability of real hardwares and without spending time in translating assembly programs to machine language.
