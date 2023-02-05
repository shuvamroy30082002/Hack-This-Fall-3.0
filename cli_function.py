from msilib import Table
import os
from os import path
import time
from datetime import datetime
from colorama import Fore,Style
import colorama
from numpy import double
from Backend.MainController import encryption
from Backend.MainController import decryption


def print_message(msg, msg_type,delay):
    '''General function to print info, Warning and error messages'''
    colorama.init(autoreset = True)
    msg_type.upper()
    current_datetime = str(datetime.now())

    if msg_type == "INFO":
            print(f'[{Fore.BLUE}{msg_type}{Fore.RESET}] {current_datetime} {Style.BRIGHT}{msg}')
            time.sleep(delay)
    elif msg_type == "WARNING":
        print(f'[{Fore.YELLOW}{msg_type}{Fore.RESET}] {Fore.YELLOW}{current_datetime} {Fore.YELLOW}{Style.BRIGHT}{msg}')
        time.sleep(delay)
    elif msg_type == "ERROR":
        print(f'[{Fore.RED}{msg_type}{Fore.RESET}] {Fore.RED}{current_datetime} {Fore.RED}{Style.BRIGHT}{msg}')
        time.sleep(delay)
    elif msg_type == "SUCCESS":
        msgtype = "INFO"
        print(f'[{Fore.BLUE}{msgtype}{Fore.RESET}]{Fore.RESET}--------------------------------------------------------------------------------------------------')
        print(f'[{Fore.BLUE}{msgtype}{Fore.RESET}] {Fore.GREEN}{current_datetime} {Fore.GREEN}{Style.BRIGHT}{msg}')
        print(f'[{Fore.BLUE}{msgtype}{Fore.RESET}]{Fore.RESET}--------------------------------------------------------------------------------------------------')

        time.sleep(delay)

def f_encrypt():
    '''Encrypt the given plain text, embed the cipher text inside the image and store it in a given location'''
    print_message("Preparing setup...","INFO",0.5)
    print_message("Press enter key to submit the input","INFO",0.5)
    global plain_text
    print("Your Plain text:")
    plain_text = str(input(f'{Fore.LIGHTCYAN_EX}'))
    if len(plain_text) == 0:
        print_message("Provide Valid Input..!","WARNING",0.5)
        return
    
    global input_length
    input_length = len(plain_text)
    global cipher_length
    global which_algo
    global process_type
    global elapsed_time
    global status
    process_type = "Encryption"
    print()
    status,cipher_length,which_algo,image,elapsed_time = encryption(plain_text)
    if status != "success":
        print_message("Unexpected error occurred!","ERROR",0)
        return
    print("Path to store the result:")
    res_path = str(input())
    print()
    if path.exists(res_path):
        if not path.isfile(res_path):
            print("Do you want to change the default name?[y/n]")
            choice = str(input())
            if choice == 'y' or choice == "Y" or choice == "Yes" or choice == "yes":
                print("Input the file name:")
                saveas = str(input())
                isdone = save_image(image,res_path,saveas)
                if isdone[0] == 1:

                    print_message(f"Image Successfully saved at {isdone[1]}!","SUCCESS",0.4)
            elif choice == 'n' or choice == 'N' or choice == 'No' or choice == 'no':
                saveas = 'vca_' + str(datetime.now().strftime("%Y%m%d_%H%M%S"))
                isdone = save_image(image = image,path=res_path,filename=saveas)
                if isdone[0] == 1:
                    print_message(f"Image Successfully saved at {isdone[1]}!","SUCCESS",0.4)
                else:
                    print_message(f"Oops! Something went wrong, Please try again","ERROR",0.5)
            else:
                print_message("Invalid choice","ERROR",0)
                return
        else:
            print_message("Should be a directory, received file!","ERROR",0)
            return
    else:
        print_message("Location not found, please provide valid path!","ERROR",0)
        return
    
def save_image(image,path,filename):
    loc = path+"/"+filename+".png"
    image.save(loc)
    return [1,loc]


def f_decrypt():
    '''Decrypt the given imaage, and extract the plain text from the cipher text'''
    global status
    global cipher_length
    global which_algo
    global elapsed_time
    global process_type
    process_type = "Decryption"

    print_message("Preparing setup...","INFO",0.5)
    print("Input the path of the Image(stego-image):")
    inp_path = str(input())
    print()
    if path.exists(inp_path):
        if path.isfile(inp_path):
            if not inp_path.lower().endswith('.png'):
                print_message("Please provide .png file only..!","ERROR",0)
                print_message("Other formats will be available soon..!","INFO",0.5)
                return
            else:
                status,cipher_length,which_algo,message,elapsed_time= decryption(inp_path)
                if status != "success":
                    print_message("Unexpected error occurred!","ERROR",0)
                    return
                print("Do you want to write plain text to a .txt file?[y/n]")
                choice = str(input())
                if choice == 'y' or choice == "Y" or choice == "Yes" or choice == "yes":
                    print("Where do yo want to store the file?")
                    file_path = str(input())
                    if path.exists(file_path):
                        if path.isfile(file_path):
                            if not file_path.lower().endswith('.txt'):
                                print_message("File format not satisfied, expected .txt format!","ERROR",0)
                                return
                            else:
                                with open(file_path,'w') as f:
                                    f.write(message)
                                print_message("Successfully copied plain text to the file!","SUCCESS",0.5)
                        elif path.isdir(file_path):
                            print("File name:")
                            file_name = str(input())
                            f = open(file_path+"\\"+file_name+".txt", "w+")
                            f.write(message)
                            f.close()
                            print_message("Successfully created and copied plain text to the file!","SUCCESS",0.5)
                        else:
                            print_message("Path is neither directory nor a file, expected any one!","ERROR",0) 
                            return
                    else:
                        print_message("Path not found!","ERROR",0)
                        return
                elif choice == 'n' or choice == "N" or choice == "No" or choice == "no":
                    print_message("Plain text retrieved Successfully!","SUCCESS",0.5)
                    print("Original Message is:")
                    print(f'{Fore.LIGHTMAGENTA_EX}{message}')
                    print()
                else:
                    print_message("Invalid choice","ERROR",0)
                    return          

        else:
            print_message("Should be a file, received directory!","ERROR",0.2)
            return

    else:
        print_message("Path not found, please provide valid path!","ERROR",0)
        return

def f_more_info():
    ''' Displays the performance aspects like elapsed time, plain_text length, cipher_text length etc.'''
    
    shape = ""
    global which_algo
    global status
    global cipher_length
    global input_length
    global elapsed_time
    global process_type
    
    if which_algo == 1:
        shape = "Octahedron"
    elif which_algo == 2:
        shape = "Hexagonal prism"
    elif which_algo == 3:
        shape = "Pentagonal Prism"
    elif which_algo == 4:
        shape = "Octagonal Prism"
    elif which_algo == 5:
        shape = "Pentagonal Pyramid"
 

        if process_type == "Encryption":
            print("1","Process type",str(process_type))
            print("2","Plain text length",str(input_length))
            print("3","Cipher text length",str(cipher_length))
            print("4","Shape used",str(shape))
            print("5","Elapsed Time",str(str(elapsed_time)+' sec'))
            print("6","Status","Completed")
        elif process_type == "Decryption":
            print("1","Process type",str(process_type))
            print("2","Cipher text length",str(cipher_length))
            print("3","Shape used",str(shape))
            print("4","Elapsed Time",str(str(elapsed_time)+' sec'))
            print("5","Status","Completed")
        else:
            print("-","No data to display","-")
            
def f_more_info():
    ''' Displays the performance aspects like elapsed time, plain_text length, cipher_text length etc.'''
    
    shape = ""
    global which_algo
    global status
    global cipher_length
    global input_length
    global elapsed_time
    global process_type
    
    if which_algo == 1:
        shape = "Octahedron"
    elif which_algo == 2:
        shape = "Hexagonal prism"
    elif which_algo == 3:
        shape = "Pentagonal Prism"
    elif which_algo == 4:
        shape = "Octagonal Prism"
    elif which_algo == 5:
        shape = "Pentagonal Pyramid"
    if status != "":
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("#", style="dim",width=6)
        table.add_column("Property",min_width=40)
        table.add_column("Value",min_width=30)

        if process_type == "Encryption":
            table.add_row("1","Process type",str(process_type))
            table.add_row("2","Plain text length",str(input_length))
            table.add_row("3","Cipher text length",str(cipher_length))
            table.add_row("4","Shape used",str(shape))
            table.add_row("5","Elapsed Time",str(str(elapsed_time)+' sec'))
            table.add_row("6","Status","Completed")
        elif process_type == "Decryption":
            table.add_row("1","Process type",str(process_type))
            table.add_row("2","Cipher text length",str(cipher_length))
            table.add_row("3","Shape used",str(shape))
            table.add_row("4","Elapsed Time",str(str(elapsed_time)+' sec'))
            table.add_row("5","Status","Completed")
        else:
            table.add_row("-","No data to display","-")
            print(table)
    print_message("Status is invalid!","Warning",0)

