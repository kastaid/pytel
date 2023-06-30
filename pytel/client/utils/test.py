from base64 import b64encode

x = "56cc080393b094f58".encode("ascii")
a = b64encode(x)
print(a)
