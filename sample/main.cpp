#include <cstring>
#include <cstdio>
#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>

int change_page_permissions_of_address(void *addr) {
    int page_size = getpagesize();
    addr -= (unsigned long)addr % page_size;

    if(mprotect(addr, page_size, PROT_READ | PROT_WRITE | PROT_EXEC) == -1) {
        return -1;
    }

    return 0;
}

int check_secret(char* secret) {
    if (strlen(secret) == 8 && secret[0] == 'M' && secret[1] == 'E')
        return 1;
    return 0;
}

void decrypt(void *addr, int key) {
    if (change_page_permissions_of_address(addr)==-1) {
         printf("change page permission error!\n");
    }

    unsigned char *start_instruction = (unsigned char*)addr;

    for (unsigned char *pos = start_instruction; pos < start_instruction + 70; ++pos) {
        *pos ^= key;
	// printf("%u ", (unsigned int)*pos);
    }
    printf("Decrypt done!\n");
}

int main(int argc, char *argv[]) {
    void *ff = (void*)check_secret;
    if (argc < 3) {
        printf("Ex: ./<prog_name> <password> <decrypt_key>\n");
        return -1;
    }

    decrypt(ff, atoi(argv[2]));

    if (argc > 1) {
        if (check_secret(argv[1])) {
            printf("password correct\n");
        }
        else {
            printf("password incorect!\n");
	    }
    }
    return 0;
}
