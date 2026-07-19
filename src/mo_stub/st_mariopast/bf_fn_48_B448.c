typedef struct {
    char pad[8];
    unsigned int p0 : 27;
    unsigned int f : 1;
} S;

void fn_48_B448(S* p) {
    p->f = 1;
}
