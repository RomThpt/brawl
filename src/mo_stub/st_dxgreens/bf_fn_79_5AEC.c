typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_79_5AEC(S* p, int v) {
    p->f = v;
}
