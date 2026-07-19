typedef struct {
    char pad[8];
    unsigned int p0 : 21;
    unsigned int f : 1;
} S;

void fn_48_B8C8(S* p) {
    p->f = 1;
}
