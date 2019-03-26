#include <stdio.h>

int main() {
	int x0 = 7, x1 = 123;
	int m = 256;
	int n = 10;
	for (int i = 0; i < n; ++i) {
		int tmp = x1;
		x1 = (x0 + x1) % m;
		x0 = tmp;
		printf("%d\n", x1);
	}
}