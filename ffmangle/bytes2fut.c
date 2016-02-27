#include <stdio.h>

int main() {
  int c;

  printf("[");
  if ((c = getc(stdin)) != EOF) {
    printf("%di8", c);
    while ((c = getc(stdin)) != EOF) {
      printf(", %di8", c);
    }
  }
  printf("]\n");
}
