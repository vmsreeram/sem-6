%{
#define	YYSTYPE	double
// #include <stdio.h>
#include "y.tab.h"
// #define NUMBER 258

// extern YYSTYPE yystype;
extern int lineno;
// extern YYSTYPE yylval;
%}

%%
[0-9]*[.]?[0-9]+    { yylval = atof(yytext); return NUMBER;}
[ '\t']             {;}
"\n"                { lineno++; return yytext[0]; }
<<EOF>>             return 0;
.                   {return yytext[0];}
%%

int yywrap(void) 
{
    return 1; 
}
// int main()
// {
//     yylex();
//     return 0;
// }