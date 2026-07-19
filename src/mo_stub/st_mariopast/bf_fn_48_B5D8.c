typedef struct {
    char pad[8];
    unsigned int p0 : 27;
    unsigned int f : 1;
} S;

void fn_48_B5D8(S* p) {
    p->f = 1;
}
