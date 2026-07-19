typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 1;
} S;

void fn_50_62D4(S* p) {
    p->f = 1;
}
