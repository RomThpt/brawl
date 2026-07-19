typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_96_1E188(S* p, int v) {
    p->f = v;
}
