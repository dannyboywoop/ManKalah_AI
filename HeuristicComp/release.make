CC=g++
CPPFLAGS= -fPIC
LDFLAGS= -shared -Wl,-soname,libgame.so 
DEPS = alphaBetaAI.h heuristic.h gameState.h heuristicComp.h
ODIR=obj
BDIR=bin
_OBJ = main.o alphaBetaAI.o heuristic.o gameState.o heuristicComp.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))
.PHONY: clean rebuild

$(ODIR)/%.o: %.cpp $(DEPS)
	$(CC) -c $< -o $@ $(CPPFLAGS)

$(BDIR)/libgame.so: $(OBJ)
	$(CC) -o $@ $(LDFLAGS) $^

clean:
	rm -f $(ODIR)/*.o
	rm -f $(BDIR)/*.out
	rm -f $(BDIR)/*.so

rebuild: clean $(BDIR)/libgame.so
	# clean then build