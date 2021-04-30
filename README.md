# Flask Framework
This is a simple web framework using Flask, serving as the middle tier of an industrial software between the serial interface and client tier.

In detail,
app.py is the main application in this project, which sends and receives different requests.

COM_2.py is a serial interface. In this specific software, it is the final step to set voltage & current for the machine.

COM_1.py is a test script to check the feasilbility of COM_2.py.

post.py is a test script simulating the requests from the client tier.

table.xls records different voltage and current for different parameters of the tested object. app.py would check it and return correct values. In the latest version, however, it is abandoned; config.dat is used instead.

config.dat is a file already applied in the software before this project starts, rather than table.xls. The file includes more than the corresponding voltage & current parameters for different sizes of pipes.

configure.txt records the parameters for the changeable serial in app.py. The path to config.dat is also recorded. The third line in this text records the time for COM_1 to sleep between the sent voltage & current, which is to ensure the serial could receive the complete messages.
