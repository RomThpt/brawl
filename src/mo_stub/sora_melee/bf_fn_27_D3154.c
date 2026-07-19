typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 1;
} S;

unsigned int fn_27_D3154(S* p) {
    return p->f;
}
