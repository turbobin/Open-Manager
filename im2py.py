import base64
open_icon = open("Myshortcut.ico","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "MYICO = '%s'\n" % b64str.decode()
f = open("icon.py","w+")
f.write(write_data)

open_icon = open("add_new.ico","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "ADDICO = '%s'" % b64str.decode()

f.write(write_data)



f.close()
