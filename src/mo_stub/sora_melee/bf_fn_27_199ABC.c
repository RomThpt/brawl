typedef struct {
    char pad[8];
    int f : 5;
} S;

int fn_27_199ABC(S* p) {
    return p->f;
}
