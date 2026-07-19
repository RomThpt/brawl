typedef struct {
    char pad[8];
    unsigned int f : 4;
} S;

void fn_79_5B90(S* p, int v) {
    p->f = v;
}
