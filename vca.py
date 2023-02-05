import click
import os
from colorama import Fore,Style
import sys
import time
import os.path
from os import close, listdir
from datetime import datetime
from os.path import isfile, join
from cli_function import * 

global prompt
cli_cmd_list = [    ['set prompt',           'f_set_prompt'   ], 
                    ['encrypt',              'f_encrypt',     ],
                    ['vca',               'f_version'        ],
                    ['decrypt',              'f_decrypt'      ],
                    ['--help',               'f_help'         ],
                    ['-h',                   'f_help'         ],
                ]

def f_help():
    '''Displays the help message'''
    print(f"""
    {Fore.LIGHTMAGENTA_EX}     encrypt{Fore.RESET}        {Style.DIM}initiate the encryption phase
    {Fore.LIGHTMAGENTA_EX}     decrypt{Fore.RESET}        {Style.DIM}initiate the decryption phase
    {Fore.LIGHTMAGENTA_EX}     set prompt{Fore.RESET}     {Style.DIM}customize the prompt text
    {Fore.LIGHTMAGENTA_EX}     show date{Fore.RESET}      {Style.DIM}displays Current date&time
    {Fore.LIGHTMAGENTA_EX}-h,  --help{Fore.RESET}         {Style.DIM}print this message.

    """)

def opening_print():
    ''' first function to be loaded and displayed'''
    colorama.init(autoreset = True)
    current_datetime = str(datetime.now())
    print()
    print(f'[{Fore.BLUE}INFO{Fore.RESET}] {current_datetime}{Style.BRIGHT} Starting VCA v0.1.0 2022..',end = '',flush=True)
    time.sleep(1)
    print('.', end = "",flush=True)
    time.sleep(1)
    print(".",end="",flush=True)
    time.sleep(1)
    print(".")


@click.command()
def vca():
    '''
    Entry point for the interface (main) function
    '''
    opening_print()
    time.sleep(0.4)
    os.system('type banner.txt')
    os.system('echo.')

    beInLoop = True
    global prompt
    prompt = 'vca'
    dollor_arrow = ' $>'
    while beInLoop:
        try:
            cli_input = input(prompt+dollor_arrow+' ')
            if cli_input == 'exit':
                print_message('Exiting....',"INFO", 0.4)
                sys.exit()

            isValid, func = isValidCmd(cli_input)

            if isValid:     
                str_to_class(func)()
            else:
                os.system(cli_input)
        except KeyboardInterrupt:
            print()
            print_message("Exiting... ","INFO", 0.4)
            sys.exit()

def isValidCmd(entered_cmd): 
    ''' Check whether command is valid or not'''  
    for c in cli_cmd_list:
        e_cmd = "".join(entered_cmd.split())
        v_cmd = "".join(str(c[0]).split())
        if e_cmd == v_cmd:
            return True, str(c[1])
    return False, entered_cmd

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

def f_set_prompt():
    '''
    Customize the prompt text, accepts 0 arguments
    '''
    global prompt
    print_message('Prompting for new prompt.',"INFO", 0.5)
    prompt = input('Enter new prompt : ')
vca()
