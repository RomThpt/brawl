typedef struct {
    char pad[8];
    unsigned int p0 : 8;
    unsigned int f : 4;
} S;

void fn_49_6F88(S* p, int v) {
    p->f = v;
}
