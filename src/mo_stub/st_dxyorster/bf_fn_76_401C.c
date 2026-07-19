typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_76_401C(S* p) {
    p->f = 1;
}
