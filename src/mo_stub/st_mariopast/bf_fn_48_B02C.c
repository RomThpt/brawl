typedef struct {
    char pad[8];
    int f : 7;
} S;

int fn_48_B02C(S* p) {
    return p->f;
}
