typedef struct {
    char pad[8];
    int f : 3;
} S;

int fn_61_E708(S* p) {
    return p->f;
}
