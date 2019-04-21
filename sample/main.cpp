#include <cstring>
#include <cstdio>
#include <stdlib.h>

#ifdef linux
#include <unistd.h>
#include <sys/mman.h>

int change_page_permissions_of_address(void *addr) {
    int page_size = getpagesize();
    addr -= (unsigned long)addr % page_size;

    if(mprotect(addr, page_size, PROT_READ | PROT_WRITE | PROT_EXEC) == -1) {
        return -1;
    }

    return 0;
}
#elif _WIN32
#include <windows.h>
int change_page_permissions_of_address(void *addr) {
    DWORD old;

    if (VirtualProtect(addr, sizeof(addr), PAGE_EXECUTE_READWRITE, &old)) {
        // printf("Writable\n");
    }
    return 0;
}
#endif

int check_secret(char* secret) {
    int signal = 0xc4397;
    if (strlen(secret) == 8 && secret[0] == 'M' && secret[1] == 'E')
        return 1;
    return 0;
}
// set this function after write secret function
int func_stub(){}

void decrypt(void *addr, int key) {
    if (change_page_permissions_of_address(addr) == -1) {
         printf("change page permission error!\n");
    }
    unsigned char *start_instruction = (unsigned char*)addr;
    unsigned char buf[200];
    int buff_pos = 0;
    void* fs = (void*)func_stub;
    int func_len = (unsigned char*)fs - (unsigned char*)addr;
    printf("func_len %d\n", func_len);

    for (unsigned char *pos = start_instruction; pos < start_instruction + func_len; ++pos) {
        // printf("%u ", (unsigned int)*pos);
        *pos ^= key;
        // printf("%u ", (unsigned int)*pos);
    }
    printf("Decrypt done!\n");
}

int main(int argc, char *argv[]) {
    void *ff = (void*)check_secret;
    int key = 9;
    if (argc < 2) {
        printf("Ex: ./<prog_name> <password>\n");
        return -1;
    }

    decrypt(ff, key);
    // printf("%s\n", "I am here!");
    if (argc > 1) {
        if (check_secret(argv[1])) {
            printf("password correct\n");
        }
        else {
            printf("password incorrect!\n");
	    }
    }
    return 0;
}
