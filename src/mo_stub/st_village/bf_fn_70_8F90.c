typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_70_8F90(S* p, int v) {
    p->f = v;
}
