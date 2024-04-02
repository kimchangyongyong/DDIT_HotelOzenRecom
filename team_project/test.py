def convertBinary(number):
    binary_representation = bin(number)[2:]  
    filled_binary = binary_representation.zfill(6)
    return filled_binary

print(convertBinary(13))

def convertLabel(cert_label):
    return "CERT_" + str(cert_label).zfill(3)

print(convertLabel(2))