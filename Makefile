MPY_CROSS_DIR = modules/circuitpython/mpy-cross
MPY_CROSS = $(MPY_CROSS_DIR)/mpy-cross
SRC := $(shell find src -type f -regex ".*\.py")
TARGETS = $(shell find src -type f -regex ".*\.py" | sed "s+src/+build/+g" | sed "s/.py/.mpy/g")
TARGET_DIR = /Volumes/CIRCUITPY

all: $(TARGETS) build/main.py

flash: all
	cp -rf build/* $(TARGET_DIR)

build/main.py: src/main.py
	cp $< $@

build/%.mpy: src/%.py 
	mkdir -p $(shell dirname $@)
	$(MPY_CROSS) -o $@ $<

$(MPY_CROSS):
	make -C $(MPY_CROSS_DIR)

copy-libs:
	cp -r modules/Adafruit_CircuitPython_ADXL34x/adafruit_adxl34x.py src/lib
	cp -r modules/Adafruit_CircuitPython_BusDevice/adafruit_bus_device src/lib

.PHONY: ensure
ensure:
	git submodule update --init --recursive
	brew install gettext python3 git
	brew link gettext --force

.PHONY: clean
clean:
	rm -rf build

