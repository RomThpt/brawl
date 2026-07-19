typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_40_24B54(S* p, int v) {
    p->f = v;
}
