#include <stdio.h>
#include <ctype.h>
#include <stdint.h>

void skipspaces() {
  int c = EOF;
  while (isspace(c = getc(stdin))) {
    /* Loop forever */
  }
  if (c != EOF) {
    ungetc(c, stdin);
  }
}

int main() {
  int c;

  skipspaces();

  if ((c = getc(stdin)) != '[') {
    return 1;
  }

  while (1) {
    uint8_t x;
    skipspaces();
    if (scanf("%di8", &x) != 1) {
      return 1;
    }
    fputc(x, stdout);
    skipspaces();
    if ((c = getc(stdin)) == ']') {
      return 0;
    }
  }
}
