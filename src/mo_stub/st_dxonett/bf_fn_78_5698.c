typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_78_5698(S* p, int v) {
    p->f = v;
}
