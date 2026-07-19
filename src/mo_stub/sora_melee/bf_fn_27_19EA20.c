typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    int f : 6;
} S;

int fn_27_19EA20(S* p) {
    return p->f;
}
