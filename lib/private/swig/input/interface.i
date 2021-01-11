
%module test1

%{
#include "speedup_performance.h"
%}

int slow_calc(int x, int a = 0, int b = 0);
