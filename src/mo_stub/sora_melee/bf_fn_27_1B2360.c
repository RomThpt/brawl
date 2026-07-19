typedef struct {
    char pad[8];
    unsigned int p0 : 14;
    int f : 7;
} S;

int fn_27_1B2360(S* p) {
    return p->f;
}
