typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_54_10148(S* p, int v) {
    p->f = v;
}
