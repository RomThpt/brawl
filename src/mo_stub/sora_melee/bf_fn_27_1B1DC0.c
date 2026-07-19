typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    int f : 6;
} S;

int fn_27_1B1DC0(S* p) {
    return p->f;
}
