# 8085 + 8255 Simulatior

Run 8085.py to run the simulator in terminal and execute machine program from *test.asm*.
#### Console Commands:
    show : display the registers values
    stba : send the strobe-a signal to the PPI
    stbb : send the strobe-b signal to the PPI
    quit : exit the program


## Documentation
### Problem Statement

As part of the subject course of Instrumentation II, the project *8085 Microprocessor and 8255 PPI Simulator* has been assigned to us. In the project, we were assigned to design a software simulating the 8085 Microprocessor and the 8255 PPI and write the software in Python language. The objective of such project was for us to familiarize in emulating an instrumentation system in software.
Additionally, we were assigned to write a program in assembly language that can:
- generate 100 random numbers in range from 00H to FFH, without repeatition
- store the random numbers in memory
- sort the random numbers in ascending order using selection sort and in descending order using bubble sort
- take the type of sorting as input from push buttons on 8255 PPI

Design Approach

The software is built in Python scripting language using Object Oriented approach. Classes representing different elements of the microprocessor and the PPI are created with appropriate methods. The project was first created to run in console by reading machine langauge program from a text file and was tested properly. Then a parser to read assembly language program and convert it to machine codes was built. Finally a graphical user interface (GUI) was added for proper user interaction.
The 8085+8255 was designed using combinations of objects of following classes:
- ALU
The Arithmetic Logic Unit is simulated using a class containing an array of registers (each storing a byte) and the methods to perform various arithmetic and logical operations like Add, Subtract, And, Or, Xor, Not etc. As with 8085, the ALU assumes one of its operand as register 'A' and can take any other byte as its second operand. For Double Addition, it assumes one of its operand as HL-register pair and can take any other double-bytes as second operand. The register array holds the general purpose registers (A, B, C, D, E, H, L), the flags (F), the program counter (PC) and the stack pointer (SP).
- CU
The Control Unit is represented using a class that hold a reference to an ALU and a Bus. It has methods to fetch, decode and execute instruction from any memory address. It can read byte from memory as addressed by the program counter (Fetch), check the byte to find out the operation to be performed (Decode) and perform the operation specified (Execute). While executing, it can fetch further instruction bytes if needed. The memory read-write and IO read-write operations are performed through the Bus. The registers of ALU are directly or indirectly used by the CU, including reading/writing to the general puspose registers, using ALU to perform operations on them, incrementing/changing program counter's value and using/modifying the stack pointer's value. Interrupts got at middle of any operation is stored and only acknowledged and handled at end of each Fetch-Decode-Execute cyle.
- Bus
It is used to address map the peripheral and memory devices using IO-mapping or memory-mapping scheme. Any device can be assigned a range of memory or IO addresses. The CU can then use the Bus to read/write data and the Bus will further use the appropriate device object to handle such data.
- RAM
RAM holds an array of bytes of size specified (by default 64K). Each byte can be read and written to using valid address. The memory bytes are accessed through the Bus.
- PPI
The 8255 PPI can be addressed as IO or memory using the Bus. The PPI stores 4 bytes in Port-A, Port-B, Port-C and Control Register. The read/write operation (performed by CU through the Bus) are handled according to the control word held in the control register. For Mode-1 and Mode-2 input operations, interrupt function objects can be assigned to the PPI, so that when strobe signal is sent, the interrupt function is called. The actual interrupt functions are implemented in the CU.

Following design pattern is used to design the overall project:
- Signal Line Representation
Interrupt and Interrupt Acknowledge signals, IO/Memory addresses and data and any other signals that can flow through hardware lines are implemented using simple function calls. Any data to be placed is sent as parameter to such function. For example, when the PPI needs to send the interrupt signal to the microprocessor, it calls the Interrupt function of the CU and the microprocessor to acknowledge the interrupt calls the Interrupt-Acknowledge function of the interrupting object.
- Byte Storage
Since Python doesn't have specific "byte" data type, just number is stored when storing a byte. Appropriate checkings are done at proper positions in the program to allow only bytes to be handled.
- Asynchronous Interrupts
Interrupts can be provided at the middle of operations. To allow this asynchronous behaviour, multithreading is used. The CU executes the operations in a different thread and the devices can provide interrupts from the main thread.
- Machine Codes
Since the machine language opcodes are too many, proper analysis to find a common pattern among the opcodes is used to simplify the programming of the CU.

The Parser is built using a single class that can read from a file any assembly or machine langauge program and convert them into each other. Process of parsing contains simple steps of:
- lexically analyzing the tokens and store the tokens in list
- syntatically analyzing the list of tokens to find errors
- converting the syntatically analyzed tokens from assembly language to machine language (or vice versa)

The GUI is built using GTK library for Python (PyGObject). The library was chosen to make the software cross platform. The GUI consists of interfaces for both 8085 and 8255. The 8085 GUI consists of buttons and displays similar to the kit in the college laboratory and can be used to input program and data to memory, to read/write from registers, to perform single step execution and to run the program from certain memory address. The 8255 GUI contains buttons to provide inputs to the ports, read outputs from the ports and strobe buttons (S1 and S2) for strobed input.

Data Sorter:
...TODO


