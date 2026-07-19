typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_77_3C78(S* p, int v) {
    p->f = v;
}
