#include "heuristicComp.h"
#include <iostream>

extern "C" {
    heuristicComp* Game_new(int depth, float north[10], float south[10]){
         return new heuristicComp(depth, north, south); 
    }
    int Game_run(heuristicComp* game){ return game->runGame(); }
}