typedef struct {
    char pad[8];
    unsigned int p0 : 16;
    unsigned int f : 8;
} S;

void fn_27_CE0AC(S* p, int v) {
    p->f = v;
}
