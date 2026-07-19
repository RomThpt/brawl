typedef struct {
    char pad[8];
    unsigned int p0 : 5;
    int f : 5;
} S;

int fn_27_1A24A0(S* p) {
    return p->f;
}
