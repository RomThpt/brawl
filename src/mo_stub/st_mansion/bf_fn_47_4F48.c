typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_47_4F48(S* p) {
    p->f = 1;
}
