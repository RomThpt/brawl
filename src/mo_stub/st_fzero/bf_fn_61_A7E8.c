typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_61_A7E8(S* p) {
    p->f = 0;
}
