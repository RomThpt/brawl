typedef struct {
    char pad[12];
    unsigned int f : 1;
} S;

unsigned int fn_27_1B1A7C(S* p) {
    return p->f;
}
