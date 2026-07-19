typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    int f : 3;
} S;

int fn_73_9F4C(S* p) {
    return p->f;
}
