typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_47_5010(S* p) {
    p->f = 1;
}
