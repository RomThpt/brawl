typedef struct {
    char pad[8];
    int f : 3;
} S;

int fn_27_19E400(S* p) {
    return p->f;
}
