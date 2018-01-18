
TARGET = test

CC = gcc

CFLAGS = -c -v -g -Wall -Wextra

VPATH = src
SRC = rosetta.c
OBJ = $(SRC:.c=.o)

all:$(TARGET)

$(TARGET):$(OBJ)
	$(CC) -o $@ $(OBJ)

.SUFFIXES: .c .o

.c.o:
	$(CC) $(CFLAGS) $<

clean:
	rm -f $(TARGET) $(TARGET)
	rm -f *.o *.obj
