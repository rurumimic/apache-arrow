#include <iostream>
#include <string>

void helloworld(std::string &s) {
  std::cout << s << std::endl;
}

int main() {
  std::string s = "Hello, World!";
  helloworld(s);
  return 0;
}

