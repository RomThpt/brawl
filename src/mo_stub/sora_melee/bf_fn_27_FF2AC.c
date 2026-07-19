typedef struct {
    char pad[8];
    int f : 3;
} S;

int fn_27_FF2AC(S* p) {
    return p->f;
}
