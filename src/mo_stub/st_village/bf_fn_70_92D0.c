typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_70_92D0(S* p) {
    p->f = 0;
}
