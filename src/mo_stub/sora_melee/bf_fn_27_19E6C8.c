typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    int f : 6;
} S;

int fn_27_19E6C8(S* p) {
    return p->f;
}
