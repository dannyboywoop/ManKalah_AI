CC=g++
CPPFLAGS= -Wall -Wswitch -W"no-deprecated-declarations" -W"empty-body" -Wconversion -W"return-type" -Wparentheses -W"no-format" -Wuninitialized -W"unreachable-code" -W"unused-function" -W"unused-value" -W"unused-variable" -O0 -fno-strict-aliasing -fno-omit-frame-pointer -fthreadsafe-statics -fexceptions -frtti -std=c++11
LDFLAGS= -Wl,--no-undefined -Wl,-z,relro -Wl,-z,now -Wl,-z,noexecstack
DEPS = alphaBetaAI.h gameState.h gameTree.h
ODIR=obj/DEBUG
BDIR=bin/DEBUG
_OBJ = main.o alphaBetaAI.o gameState.o gameTree.o client.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.cpp $(DEPS)
	$(CC) -c -x c++ $< -g2 -gdwarf-2 -o $@ $(CPPFLAGS)

$(BDIR)/MankalahAIDEBUG.out: $(OBJ)
	$(CC) -o $@ $(LDFLAGS) $^

clean:
	rm -f $(ODIR)/*.o
	rm -f $(BDIR)/*.out