# SIMBLE Window Manager Makefile
CXX = g++
CXXFLAGS = -Wall -Wextra -O2
LIBS = -lX11 -lXft -lfontconfig

TARGET = simble
SRC = main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET) $(LIBS)

clean:
	rm -f $(TARGET)

run: all
	# Jalanin Xephyr di display :1 dengan resolusi 800x600
	Xephyr -br -ac -noreset -screen 800x600 :1 & \
	sleep 1; \
	DISPLAY=:1 ./$(TARGET)

.PHONY: all clean run
