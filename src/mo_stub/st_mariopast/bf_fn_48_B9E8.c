typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_48_B9E8(S* p, int v) {
    p->f = v;
}
