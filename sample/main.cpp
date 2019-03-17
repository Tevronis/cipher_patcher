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
    if (strlen(secret) == 8 && secret[0] == 'M' && secret[1] == 'E')
        return 1;
    return 0;
}

void decrypt(void *addr, int key, int func_len) {
    if (change_page_permissions_of_address(addr)==-1) {
         printf("change page permission error!\n");
    }

    unsigned char *start_instruction = (unsigned char*)addr;

    for (unsigned char *pos = start_instruction; pos < start_instruction + func_len; ++pos) {
        // printf("%u ", (unsigned int)*pos);
        *pos ^= key;
    }
    printf("Decrypt done!\n");
}

int main(int argc, char *argv[]) {
    void *ff = (void*)check_secret;
    if (argc < 4) {
        printf("Ex: ./<prog_name> <password> <decrypt_key> <len_of_decrypted_function>\n");
        return -1;
    }

    decrypt(ff, atoi(argv[2]), atoi(argv[3]));

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
