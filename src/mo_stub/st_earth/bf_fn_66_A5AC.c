typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 2;
} S;

int fn_66_A5AC(S* p) {
    return p->f;
}
