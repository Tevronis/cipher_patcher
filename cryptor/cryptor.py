# -*- coding: utf-8 -*-
import os

import pefile
import pyelftools

def pe_elf():
    pass


def pe_exe():
    pe_filename = input('Enter file name:\n>')
    if os.path.isfile(pe_filename):
        pe = pefile.PE(name=pe_filename, fast_load=True)
        try:
            pass
        except pefile.PEFormatError:
            print('pefile.PEFormatError')
            return False
        except PermissionError:
            print('Permission error to file: {}'.format(pe_filename))
            return False
        if pe.is_dll():
            print('Does not support dll format')
            exit()
        print('Address of Entry Point = %s'.format(hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)))
        pe.parse_data_directories()
        for d_dir in pe.OPTIONAL_HEADER.DATA_DIRECTORY:
            print(d_dir)

        code_section = None
        for section in pe.sections:
            if hex(section.Characteristics) == '0x60000020':  # если секция явялется секцией кода
                code_section = section.get_data()

                break


if __name__ == '__main__':
    main()