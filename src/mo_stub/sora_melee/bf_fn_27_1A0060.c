typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_27_1A0060(S* p, int v) {
    p->f = v;
}
