typedef struct {
    char pad[8];
    unsigned int f : 8;
} S;

void fn_27_D1194(S* p, int v) {
    p->f = v;
}
