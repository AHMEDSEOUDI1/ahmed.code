Delimiter= "message ends here"
def main():
    while True:
        print("Stenography project Coventry")
        print("1.Hide a message in picture")
        print("2.get a secret message from picture")
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
    print("##########Encoding in progress##########")
    Pic_Path = input("enter the path for your pic")
    pic_path_after_encode = input("enter pic path after encode")
    if not pic_path_after_encode.lower().endswith(".bmp"):
        pic_path_after_encode += "encoded.bmp"
    print("1.enter your hidden message")
    print("2.get text from file")
    selection = input("select a number")
    if selection == "1":
        hidden_message = input("enter your hidden message")
    elif selection == "2":
        file = input("write file path")
        hidden_message = RT(file) # (Read text file)
    else:
        print("enter a valid selection")  
        return

    msg_bytes = s_to_b(hidden_message)  #RB(Read binary file)
    delimiter_bytes = s_to_b(Delimiter)
    p_load_bytes = msg_bytes + delimiter_bytes
    p_l_bits = byte_to_bit(p_load_bytes) #p_l_bits = pay load bits
    pic_bytes = RB(Pic_Path) # S_TO B(STRING TO BYTES)
    data_offset = Get_D_O (pic_bytes) #D_O(DATA OFFSET)
    #########ENCODE#######################
    free_space = len(pic_bytes) - data_offset
    required = len(p_l_bits)
    if required > free_space:
         print("no free space")
         return
    output = bytearray(pic_bytes)
    index = 0 
    for i in range(data_offset,len(output)):
         if index >= required:
              break
         else:
              output[i] = set_least_sig_bit(output[i],p_l_bits[index])
              index+=1
    
    type_binary_file(pic_path_after_encode,output)
    print(f"hidden message in {pic_path_after_encode}")
    

######################################decoding#########################
def decode():
     print("DECODING IN PROGRESS")
     path_after_encode = input("enter the path of the encoded pic to get the hidden message")
     pic_bytes = RB(path_after_encode)
     D_O = Get_D_O(pic_bytes) # D_O = DATA OFFSET 
     delimiter_bytes = s_to_b(Delimiter)
     delimiter_bits = byte_to_bit(delimiter_bytes)
     delimiter_legth = len(delimiter_bits)
     combinedbits = []
     for i in range(D_O,len(pic_bytes)):
          combinedbits.append(get_leat_sig_bit(pic_bytes[i]))
          if len(combinedbits) >= delimiter_legth:
               if combinedbits[-delimiter_legth:] == delimiter_bits:
                hidden_msg_bits = combinedbits[:-delimiter_legth]
                hidden_msg_bytes = bits_to_bytes(hidden_msg_bits)
                final = byte_to_strg(hidden_msg_bytes)
                print(f"your hidden message is :{final}")
                return
     print("the pic has no hidden message in it")      
######################get_lest_significant_bit############################
def get_leat_sig_bit(byte):
     return byte & 1
###############################set_least_sig_bit##########################
def set_least_sig_bit(byte,bit):
     return (byte & 0b11111110) | ( bit & 1)
############byte to string####################################
def byte_to_strg(byte):
     return bytes(byte).decode("utf-8",errors = "ignore") 
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
    ###########################read binary file#############read pic bites
def RB(P):   # P= PATH  D=DATA
    F = open(P,"rb") # F= FILE
    D = F.read() # D = DATA
    F.close()
    return D 
    ###########################write binary file#############to save new pic with hid msg
def type_binary_file(P,D):   # P= PATH  D=DATA
        F = open(P,"wb") # F= FILE
        F.write(D) # D = DATA
        F.close() 
###########################Data Offset#############indicator
def Get_D_O(bytes):
     A = bytes[10]
     B = bytes[11]
     C = bytes[12]
     D = bytes[13]
     return A + (B << 8 ) + (C << 16) + (D << 24)
##############string to bytes########################
def s_to_b(string):
     return list(string.encode("utf-8"))
###############bytes to bits############################
def byte_to_bit(byte):
     bits = []
     for x in byte:
          for y in range (7,-1,-1):
               bits.append((x>>y)&1)
     return bits
######################bits to bytes####################
def bits_to_bytes(bit): 
     if len(bit) % 8 != 0:
       raise ValueError ("must be a mult of 8 ")
     
     message = []
     for i in range(0,len(bit),8):
          b = 0
          for j in range(8):
               b = (b<<1) | (bit[i+j] & 1)
          message.append(b)
     return message

main()