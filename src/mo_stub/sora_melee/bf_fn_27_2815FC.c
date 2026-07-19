typedef struct {
    char pad[44];
    unsigned int p0 : 17;
    int f : 8;
} S;

int fn_27_2815FC(S* p) {
    return p->f;
}
