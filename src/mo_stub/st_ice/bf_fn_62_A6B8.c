typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_62_A6B8(S* p) {
    p->f = 1;
}
