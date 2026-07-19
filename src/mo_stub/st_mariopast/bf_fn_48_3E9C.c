typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_48_3E9C(S* p, int v) {
    p->f = v;
}
