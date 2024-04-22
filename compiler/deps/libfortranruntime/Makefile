SOURCE = /llvm/deps/llvm-project
BUILD = /llvm/build

RUNTIME_SOURCES := $(wildcard $(SOURCE)/flang/runtime/*.cpp)
RUNTIME_SOURCES += $(SOURCE)/flang/lib/Decimal/decimal-to-binary.cpp
RUNTIME_SOURCES += $(SOURCE)/flang/lib/Decimal/binary-to-decimal.cpp
RUNTIME_OBJECTS = $(patsubst $(SOURCE)/%,$(BUILD)/%,$(RUNTIME_SOURCES:.cpp=.o))

RUNTIME_CXXFLAGS += -I$(BUILD)/include -I$(BUILD)/tools/flang/runtime
RUNTIME_CXXFLAGS += -I$(SOURCE)/flang/include -I$(SOURCE)/llvm/include
RUNTIME_CXXFLAGS += -DFLANG_LITTLE_ENDIAN
RUNTIME_CXXFLAGS += -fPIC -Wno-c++11-narrowing -fvisibility=hidden
RUNTIME_CXXFLAGS += -DFE_UNDERFLOW=0 -DFE_OVERFLOW=0 -DFE_INEXACT=0
RUNTIME_CXXFLAGS += -DFE_INVALID=0 -DFE_DIVBYZERO=0 -DFE_ALL_EXCEPT=0

$(BUILD)/flang/runtime/libFortranRuntime.a: $(RUNTIME_OBJECTS)
	@rm -f $@
	emar -rcs $@ $^

$(BUILD)%.o : $(SOURCE)%.cpp
	@mkdir -p $(@D)
	em++ $(RUNTIME_CXXFLAGS) -o $@ -c $<

.PHONY: clean
clean:
	@rm $(RUNTIME_OBJECTS) $(BUILD)/flang/runtime/libFortranRuntime.a

.PHONY: build
build: $(BUILD)/flang/runtime/libFortranRuntime.a
