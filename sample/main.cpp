#include <cstring>
#include <cstdio>

int check_secret(char* secret) {
    if (strlen(secret) == 3)
        return 1;
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        if (check_secret(argv[1])) {
            printf("password correct");
        }
    }
    return 0;
}