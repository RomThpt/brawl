typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 4;
} S;

int fn_56_6798(S* p) {
    return p->f;
}
