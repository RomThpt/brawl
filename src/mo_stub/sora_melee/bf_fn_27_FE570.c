typedef struct {
    char pad[8];
    unsigned int p0 : 9;
    unsigned int f : 1;
} S;

unsigned int fn_27_FE570(S* p) {
    return p->f;
}
