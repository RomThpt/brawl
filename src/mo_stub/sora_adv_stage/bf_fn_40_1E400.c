typedef struct {
    char pad[8];
    int f : 6;
} S;

int fn_40_1E400(S* p) {
    return p->f;
}
