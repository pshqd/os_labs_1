CC      = g++
CFLAGS  = -Wall -Wextra -pedantic -fPIC
TARGET  = libcaesar.so
SRC     = caesar.cpp
INSTALL_DIR = /usr/local/lib
TEST_SCRIPT = test_caesar.py
INPUT   = input.txt
OUTPUT  = output.txt
KEY     = 42

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -shared -o $(TARGET) $(SRC)

install: $(TARGET)
	mkdir -p $(INSTALL_DIR)
	cp $(TARGET) $(INSTALL_DIR)/$(TARGET)
	@if command -v ldconfig > /dev/null 2>&1; then ldconfig; fi

test: $(TARGET)
	python3 $(TEST_SCRIPT) ./$(TARGET) $(KEY) $(INPUT) $(OUTPUT)

clean:
	rm -f $(TARGET) $(OUTPUT)

.PHONY: all install test clean
