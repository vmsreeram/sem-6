all: a.out

a.out: calculator.y calculator.l
	yacc -d calculator.y && lex calculator.l && gcc -Wno-error=all lex.yy.c y.tab.c

clean:
	@rm -f a.out y.tab.c y.tab.h lex.yy.c