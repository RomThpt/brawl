typedef struct {
    char pad[8];
    unsigned int f : 10;
} S;

void fn_27_1A6C54(S* p, int v) {
    p->f = v;
}
