BOARD ?= esp32:esp32:waveshare_esp32_s3_zero
PORT  ?= /dev/cu.usbmodem101
BUILD_DIR ?= build

# extra build properties (like "Use CDC on Boot")
BUILD_PROPS ?= :CDCOnBoot=cdc

.PHONY: default all flash clean

default: all flash

all:
	arduino-cli compile --fqbn $(BOARD)$(BUILD_PROPS) ./ --output-dir build
flash: all
	arduino-cli upload --fqbn $(BOARD) --port $(PORT) --input-dir $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR)

