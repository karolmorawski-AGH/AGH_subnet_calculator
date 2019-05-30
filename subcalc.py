import sys
import os
from array import *
import re
import subprocess

#----------------------------------------------------
#Main functions for displaying output, getting input and pinging
def calculate(adress):
    ip = '.'.join(map(str, adress[0:4]))
    mask = ip.join(map(str,adress[4:]))

    #network address
    net_addr = get_network_adress(ip_to_binary(adress), mask_to_binary(int(mask)))
    #broadcast address
    broad_addr = get_broadcast(ip_to_binary(adress), mask_to_binary(int(mask)))

    ip_content = "IP Address: \t\t" + ip + "\t\t" + binary_to_string(ip_to_binary(adress))
    cidr = "CIDR: \t\t\t" + mask + "\t\t\t" + binary_to_string(mask_to_binary(int(mask)))
    network_address = "Network adress \t\t" + binary_to_decimal(net_addr) + "\t\t" + binary_to_string(net_addr)
    network_class = "Network class: \t\t" + get_network_class(ip_to_binary(adress))
    network_type = "Network type: \t\t" + pool_determination(adress[0:4])
    network_mask = "Network mask: \t\t" + binary_to_decimal(mask_to_binary(int(mask))) + "\t\t" + binary_to_string(mask_to_binary(int(mask)))
    broadcast_address = "Broadcast address: \t" + binary_to_decimal(broad_addr) + "\t\t" + binary_to_string(broad_addr)
    first_host_address = "First host address: \t" + binary_to_decimal(get_first_host(net_addr)) + "\t\t" + binary_to_string(get_first_host(net_addr))
    last_host_address = "Last host address: \t" + binary_to_decimal(get_last_host(broad_addr)) + "\t\t" + binary_to_string(get_last_host(broad_addr))
    max_host_number = "Max number of hosts: \t" + get_max_hosts(mask_to_binary(int(mask)))
    
    #print info on terminal
    print("\n" + ip_content)
    print(cidr)
    print(network_address)
    print(network_class)
    print(network_type)
    print(network_mask)
    print(broadcast_address)
    print(first_host_address)
    print(last_host_address)
    print(max_host_number)

    #adding output to list which is then utilized by write_output
    array_output = []

    array_output.append(ip_content + "\n")
    array_output.append(cidr + "\n")
    array_output.append(network_address + "\n")
    array_output.append(network_class + "\n")
    array_output.append(network_type + "\n")
    array_output.append(network_mask + "\n")
    array_output.append(broadcast_address + "\n")
    array_output.append(first_host_address + "\n")
    array_output.append(last_host_address + "\n")
    array_output.append(max_host_number + "\n")
   
    write_output(array_output)
  
    if((ip != binary_to_decimal(net_addr)) and ip != binary_to_decimal(broad_addr)):
        anwser = input("Do you want to ping this address? (y/n)")
        if anwser == 'y':
           ping(ip)


def write_output(output_array):
    print("\nWriting output to file -> 'subcalc_output.txt'")

    file = open('subcalc_output.txt', 'w')
    file.writelines(output_array)
    file.close()

def ping(address):
    if(os.name == "posix"):
        command = ['ping', '-c', '5', address]
    elif(os.name == "nt"):
        command = ['ping', address]

    subprocess.call(command)
#----------------------------------------------------

#----------------------------------------------------
#Calculating functions - bitwise operations

#Binary to decimal binary format
def binary_to_string(adress):
    
    return_val = ""

    #octets processed one by one
    first = adress[:8]
    second = adress[8:16]
    third = adress[16:24]
    fourth = adress[24:]

    return_val = first + "."  + second + "." + third + "." + fourth
    return return_val

#casts adress as binary number
def ip_to_binary(adress):
    binary_ip = []

    for i in range(len(adress)-1): 
        binary_ip.append(format(adress[i], '#010b')[2:])
    binary_ip = ''.join(binary_ip)
    return binary_ip

#casts mask as binary number
def mask_to_binary(cidr):
    rest = 32 - cidr
    binary_string = ""

    for i in range(cidr):
        binary_string = binary_string + "1"

    for i in range(rest):
        binary_string = binary_string + "0" 

    return binary_string

def get_network_adress(bin_ip, bin_mask):

    if(len(bin_ip) != len(bin_mask)):
        print("ERROR: IP and MASK have different binary representation AT get_network_adress()")
        return

    binary_network = ""
    #Bitwise AND but on strings
    for i in range(32):
        if((bin_mask[i] == '1') and (bin_ip[i] == '1')):
            binary_network = binary_network + "1"
        else:
            binary_network = binary_network + "0"

    return binary_network

#broadcast address
def get_broadcast(bin_ip, bin_mask):
    
    #Wildcard
    wildcard = ""
    for i in range(32):
        if(bin_mask[i] == "1"):
            wildcard = wildcard + "0"
        else:
            wildcard = wildcard + "1"

    #Bitwise OR but on strings
    network_addr = ""
    for i in range(32):
        if(wildcard[i] == "0" and bin_ip[i] == "0"):
            network_addr = network_addr + "0"
        else:
            network_addr = network_addr + "1"

    return network_addr

#first host number
def get_first_host(net_addr):
    first_host = net_addr[:31] + "1"
    return first_host

#last host number
def get_last_host(broad_addr):
    if(broad_addr == "11111111111111111111111111111111"):
        return broad_addr
    
    last_octet = int(broad_addr,2) - 1 
    last_octet = format(last_octet, '#08b')[2:]

    if(len(last_octet) < 32):
        for i in range(32 - len(last_octet)):
            last_octet = "0" + last_octet

    last_host = last_octet
    return last_host

#max number of host
def get_max_hosts(bin_mask):
    mask = int(bin_mask,2)

    #wildcard
    wildcard = 0b11111111111111111111111111111111 - mask
    host_max = wildcard - 0b000000000000000000000001
    host_max = int(host_max)

    #For 255.255.255.255/32
    if(host_max == -1):
        host_max = 1

    return str(host_max)


#binary to dec
def binary_to_decimal(adress):

    return_val = ""

    #octets processed one by one
    first = int(adress[:8],2)
    second = int(adress[8:16],2)
    third = int(adress[16:24],2)
    fourth = int(adress[24:32],2)

    return_val = str(first) + "."  + str(second) + "." + str(third) + "." + str(fourth)
    return return_val

#----------------------------------------------------

#----------------------------------------------------
#Checks whether given address and mask is correct - returns array of dotted decimal address e.g. 192.168.0.1/24 -> [192, 168, 0, 1, 24]

def check_adress(adress):
    #Checking if string contains '.' and '/'
    argument = adress
    dotcount = 0
    slashcount = 0
    #Checking number of separators
    for char in argument:
        if char == ".":
            dotcount = dotcount + 1
        if char == "/":
            slashcount = slashcount + 1
    if dotcount != 3 or slashcount != 1:
        print("ERROR: Invalid argument")
        sys.exit()
    #Adding various things to array
    tosplit = argument.split('/')
    mask = tosplit[1]
    ip = tosplit[0].split('.')
    #Checks if there are only numeric characters in string
    if(mask.isdigit() != True):
        print("ERROR: Invalid mask")
        sys.exit()
    for record in ip:
        if(record.isdigit() != True):
            print("ERROR: Invalid IPv4")
            sys.exit()
    if(int(mask) < 0 or int(mask) > 32 ):
        print("ERROR: Invalid Netmask")
        sys.exit()
    for record in ip:
        if(int(record) > 255 or int(record) < 0):
            print("ERROR: Invalid IPv4")
            sys.exit()
    #returning array of numeric values
    mask = int(mask)
    ip = list(map(int, ip))
    return_val = []
    return_val.extend(ip)
    return_val.append(mask)
    return return_val
#----------------------------------------------------

#----------------------------------------------------
#Non bitwise operations calculating network specific information

#Gets newtork class
def get_network_class(bin_ip):
    #looking only at the first octet
    first_octet = bin_ip[0:8]
    first_octet = int(first_octet,2)

    #Class A
    if(first_octet < 128):
        return "A"
    elif (first_octet<192):
        return "B"
    elif (first_octet<224):
        return "C"
    elif (first_octet<240):
        return "D"
    else:
        return "E"

#Gets pool type
def pool_determination(ip):
    if(ip[0] == 10):
        return "Private"
    elif(ip[0]==172 and (ip[1] in range(16,31))):
        return "Private"
    elif(ip[0]==192 and ip[1]==168):
        return "Private"
    else:
        return "Public"
#----------------------------------------------------

#----------------------------------------------------
#Getting network IP address and mask

#Gets network address - os specific
def get_adress():
    if(os.name == "posix"):
       return get_linux_adress()
    elif(os.name == "nt"):
      return  get_windows_adress()

#Gets network address - Windows
def get_windows_adress():
    cmd = "ipconfig"
    cli = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = cli.communicate()[0]
    output = str(output)
    output = output.split("\\r\\n")
    ip_array = []
    mask_array = []
    for i in range(len(output)):
        if("IPv4 Address" in output[i]):
            ip = output[i].split(": ")
            mask = output[i+1].split(": ")
            mask = mask_to_bits(mask[1])
            ip_array.append(ip[1])
            mask_array.append(mask)
    #gets last record from array
    ip = ip_array[len(ip_array)-1]
    mask = mask_array[len(mask_array)-1]
    return_val = ip + "/" + mask
    return return_val

#Gets network address - Linux  
def get_linux_adress():
    #"ip -o -f inet addr show | awk '{ print $4 }'"
    cmd = "ip -o -f inet addr show | awk '{ print $4 }'"
    cli = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = cli.communicate()[0]
    output = str(output)
    output = output.split("\\n")
    #removing "b'" which indicates output was byte sequence
    output[0] = output[0][2:]
    #returning string which is then double cheked by check_adress()
    return output[0]

#Used in get_windows_adress in order not to have 2 different functions for calculating masks
def mask_to_bits(mask):
    mask = mask.split(".")
    mask_string = []
    for val in mask:
        val = int(val)
        mask_string.append(bin(val))
    #making a string from array
    values = ''.join(mask_string)
    one_count = 0
    for char in values:
        if(char == "1"):
            one_count = one_count+1
    return str(one_count)
#----------------------------------------------------


#Main
if len(sys.argv) == 1:
    ip = check_adress(get_adress())
    calculate(ip)
elif len(sys.argv) == 2:
    ip = check_adress(sys.argv[1])
    calculate(ip)
else:
    print("WARNING: Only first argument will be considered\n")
    ip = check_adress(sys.argv[1])
    calculate(ip)