typedef struct {
    char pad[8];
    unsigned int p0 : 16;
    int f : 8;
} S;

int fn_27_D1208(S* p) {
    return p->f;
}
