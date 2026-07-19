typedef struct {
    char pad[8];
    unsigned int f : 3;
} S;

void fn_62_60E4(S* p, int v) {
    p->f = v;
}
