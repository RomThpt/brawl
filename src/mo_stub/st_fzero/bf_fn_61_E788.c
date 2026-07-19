typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    int f : 3;
} S;

int fn_61_E788(S* p) {
    return p->f;
}
