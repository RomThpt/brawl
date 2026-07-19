typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    unsigned int f : 9;
} S;

void fn_48_B428(S* p, int v) {
    p->f = v;
}
