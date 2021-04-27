# Flask Framework
This is a simple web framework using Flask, serving as the middle tier of an industrial software between the serial interface and client tier.

In detail,
app.py is the main application in this project, which sends and receives different requests.

COM_2.py is a serial interface. In this specific software, it is the final step to set voltage & current for the machine.

COM_1.py is a test script to check the feasilbility of COM_2.py.

post.py is a test script simulating the requests from the client tier.

app_sample.py and post_sample.py are sample scripts offered as samples.

table.xls records different voltage and current for different parameters of the tested object. app.py would check it and return correct values to the serial, as well as the client.

configure.txt records the parameters for the changeable serial in app.py.
