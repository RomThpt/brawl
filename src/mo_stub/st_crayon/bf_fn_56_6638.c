typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 1;
} S;

void fn_56_6638(S* p) {
    p->f = 1;
}
