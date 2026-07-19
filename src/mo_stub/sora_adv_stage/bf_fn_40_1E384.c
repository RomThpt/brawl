typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    unsigned int f : 1;
} S;

void fn_40_1E384(S* p) {
    p->f = 1;
}
