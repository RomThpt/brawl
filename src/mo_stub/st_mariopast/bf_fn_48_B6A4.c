typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    int f : 9;
} S;

int fn_48_B6A4(S* p) {
    return p->f;
}
