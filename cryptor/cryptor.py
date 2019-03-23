#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import collections
import pefile
import itertools
from tornado.template import Template

FASM_PATH = r'C:\Projects\cipher_patcher\cryptor\fasm\fasmw17139_win\FASM.EXE'
Config = collections.namedtuple('Config', 'algorithm acm_payload filename key')

DIR_PATH = 'cryptor/'


def xor_crypt(section, key):
    section.xor_data(key)


def xor_gamma_crypt(section, key):
    data = section.get_data()
    new_data = ""
    gen = itertools.cycle(key)
    for b in data:
        if b:
            new_data += chr(ord(b) ^ int(next(gen)))
        else:
            new_data += "\x00"

    section.pe.data_replace(section.PointerToRawData, new_data)


def print_pe_info(pe):
    pass


def run(config):
    pe = pefile.PE(config.filename)

    pe.add_last_section(size=1024)

    config.algorithm(pe.sections[0], key=config.key)

    # add first 512 bytes from first section to last (new) section
    pe.data_copy(pe.sections[0].PointerToRawData, pe.sections[-1].PointerToRawData, 512)

    # simple payload. just execute jump in last section
    asm = Template(open('{}pack.tpl.asm'.format(DIR_PATH), 'r').read()).generate(
        go=pe.OPTIONAL_HEADER.ImageBase + pe.sections[-1].VirtualAddress + 512,
    )

    with open('{}pack.asm'.format(DIR_PATH), 'w') as f:
        f.write(asm)
    os.system('{} {}pack.asm'.format(FASM_PATH, DIR_PATH))

    # write, decode and jump to original code
    asm = Template(open(config.acm_payload, 'r').read()).generate(
        copy_from=pe.OPTIONAL_HEADER.ImageBase + pe.sections[-1].VirtualAddress,
        copy_to=pe.OPTIONAL_HEADER.ImageBase + pe.sections[0].VirtualAddress,
        copy_len=512,
        xor_len=pe.sections[0].Misc_VirtualSize,
        key_encode=config.key,
        original_eop=pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.AddressOfEntryPoint,
    )
    with open('{}copy.asm'.format(DIR_PATH), 'w') as f:
        f.write(asm)
    os.system(r'{} {}copy.asm'.format(FASM_PATH, DIR_PATH))

    new_pack = open('{}pack.bin'.format(DIR_PATH), 'rb').read()
    new_copy = open('{}copy.bin'.format(DIR_PATH), 'rb').read()

    pe.OPTIONAL_HEADER.AddressOfEntryPoint = pe.sections[0].VirtualAddress
    print(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    pe.data_replace(offset=pe.sections[0].PointerToRawData, new_data=new_pack)
    print(pe.sections[0].PointerToRawData)
    pe.data_replace(offset=pe.sections[-1].PointerToRawData + 512, new_data=new_copy)

    pe.sections[0].Characteristics |= pefile.SECTION_CHARACTERISTICS['IMAGE_SCN_MEM_WRITE']

    pe.write(filename='result.exe')


if __name__ == '__main__':
    xor_config = Config(xor_crypt, '{}copy.tpl.asm'.format(DIR_PATH), sys.argv[-2], int(sys.argv[-1]))
    xor_gamma_config = Config(xor_gamma_crypt, '{}gamma_xor.acm'.format(DIR_PATH), sys.argv[-2], int(sys.argv[-1]))
    if '-x' in sys.argv:
        run(xor_config)
    elif '-gx' in sys.argv:
        run(xor_gamma_config)
