typedef struct {
    char pad[8];
    unsigned int p0 : 16;
    int f : 8;
} S;

int fn_27_D13A0(S* p) {
    return p->f;
}
