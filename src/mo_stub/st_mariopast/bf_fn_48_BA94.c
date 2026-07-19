typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 6;
} S;

void fn_48_BA94(S* p, int v) {
    p->f = v;
}
