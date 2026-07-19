typedef struct {
    char pad[8];
    unsigned int f : 9;
} S;

void fn_48_B4D0(S* p, int v) {
    p->f = v;
}
