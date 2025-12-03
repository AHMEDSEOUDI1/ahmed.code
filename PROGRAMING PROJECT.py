def main():
    while True:
        print("Stgnography project Coventry")
        print("1.Hide a message in pic")
        print("2.get message from pic")
        print("3.exit")
        selection = input("pick a choice")
        if selection == "1":
            Encode()
        elif selection == "2":
            decode()    
        elif selection =="3":
            break
        else:
            print("Choose a valid input")    
#Encoding
def Encode():
    print("##########Encodind in progress##########")
    Pic_Path = input("enter the path for your pic")
    pic_path_after_encode = input("enter pic path after encoded")
    print("1.enter your hidden message")
    print("2.get text from file")
    selection = input("select a number")
    if selection == "1":
        hidden_message = input("enter your hidden message")
    elif selection == "2":
        file_path = input("write file path")
        hidden_message = R_T(Pic_Path) # (Read text file)
    else:
        print("enter a valid selection")  
        return

    pic_bytes = RB(Pic_Path)  #RB(Read binary file)
    MSG_bytes = S_TO_B(pic_bytes) # S_TO B(STRING TO BYTES)
    data_offset = Get_D_O (pic_bytes) #D_O(DATA OFFSET)
    MSG_bytes = S_TO_B(pic_bytes)
    delimiter_bytes = string_to_bytes(delimiter)
    payload_bytes = MSG_bytes + delimiter_bytes
    payload_bits = bytes_to_bits(payload_bytes)
    #########ENCODE#######################
    free_space = len(pic_bytes) - data_offset
    required = len(payload_bits)
    if required > free_space:
         print("no free space")
         return
    output = bytearray(pic_bytes)
    index = 0 
    for i in range(data_offset,len(output)):
         if index >= required:
              break
         else:
              output[i] = set_lsb(output[i],payload_bits[index])
              index+=1
    
    type_binary_file(pic_path_after_encode,Encode)
    print("hidden message")
    

######################################decoding#########################
def decode():
     print("DECODING IN PROGRESS")
     path_after_encode = input("enter the path of the encoded pic to get the hidden message")
     pic_bytes = read_B_F(path_after_encode)
     D_O = Get_D_O(pic_bytes) # D_O = DATA OFFSET 
     delimiter_bits = bytes_to_bits(string_to_bytes(delimiter))
     delimiter_legth = len(delimiter_bits)
     combinedbits = []
     for i in range(D_O,len(pic_bytes)):
          bit = get_lsb(pic_bytes[i])
          combinedbits.append(bit)
          if len(combinedbits) >= delimiter_legth:
               hidden_msg_bits = combinedbits[:-delimiter_legth]
               hidden_msg_bytes = bits_to_bytes(hidden_msg_bits)
               final = byte_to_strg(hidden_msg_bytes)
               print(f"your hidden message is :{final}")
               return
    print("the pic has no hidden message in it")      
######################get_lest_significant_bit############################
def get_leat_sig_bit(byte):
     return(byte & 1)
###############################set_least_sig_bit##########################
def set_least_sig_bit(byte,bit):
     return (byte & 0b11111110)
############byte to string####################################
def byte_to_strg(byte):
     return bytes(byte).decode("utf-8",errors = "IGNORE") 
##############READ TEXT FILE#######################
def read_file(path):
     file = open(path,"r",encoding = "utf-8")
     data = file.read()
     file.close()
     return data

    #############read text file####################
def RT(path): #R_T (READ TEXT FILE)
        F = open(path,"r",encoding = "utf-8")
        D = F.read() # D = DATA
        F.close() 
        return D
    ###########################read binary file#############
def RB(P):   # P= PATH  D=DATA
    F = open(P,"rb") # F= FILE
    D = F.read() # D = DATA
    F.close()
    return D 
    ###########################write binary file#############
def type_binary_file(P,D):   # P= PATH  D=DATA
        F = open(P,"wb") # F= FILE
        F.write(D) # D = DATA
        F.close() 
###########################Data Offset#############
def Get_D_O(bytes):
     D1 = bytes[10]
     D2 = bytes[11]
     D3 = bytes[12]
     D4 = bytes[13]
     return D1 + (D2 <<8 ) + (D3 << 16) + (D4 << 24)
##############string to bytes########################
def string_to_bytes(string):
     return list(string.encode("utf-8"))
###############bytes to bits############################
def byte_to_bit(byte):
     bits = []
     for i in byte:
          for j in range (7,-1,-1):
               bits.append((i>>j)&1)
               return bits
######################bits to bytes####################
def bits_to_bytes(bit): 
     if len(bit) % 8 != 0:
       raise ValueError ("must be a mult of 8 ")
     
     output = []
     for i in range(0,len(bit))