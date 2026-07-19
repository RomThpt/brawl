typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    unsigned int f : 4;
} S;

void fn_54_6984(S* p, int v) {
    p->f = v;
}
