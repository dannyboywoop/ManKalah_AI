CC=g++
CPPFLAGS= -Wall -Wswitch -W"no-deprecated-declarations" -W"empty-body" -Wconversion -W"return-type" -Wparentheses -W"no-format" -Wuninitialized -W"unreachable-code" -W"unused-function" -W"unused-value" -W"unused-variable" -O3 -fno-strict-aliasing -fomit-frame-pointer -DNDEBUG -fthreadsafe-statics -fexceptions -frtti -std=c++11
LDFLAGS= -Wl,--no-undefined -Wl,-z,relro -Wl,-z,now -Wl,-z,noexecstack
DEPS = alphaBetaAI.h gameState.h gameTree.h TCPGameEngine.h message.h heuristic.h
ODIR=obj/TCP
BDIR=bin/TCP
_OBJ = TCPmain.o alphaBetaAI.o gameState.o gameTree.o TCPGameEngine.o message.o heuristic.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))
.PHONY: clean rebuild

$(ODIR)/%.o: %.cpp $(DEPS)
	$(CC) -c -x c++ $< -g1 -o $@ $(CPPFLAGS)

$(BDIR)/MankalahAI.out: $(OBJ)
	$(CC) -o $@ $(LDFLAGS) $^

clean:
	rm -f $(ODIR)/*.o
	rm -f $(BDIR)/*.out

rebuild: clean $(BDIR)/MankalahAI.out
	# clean then build