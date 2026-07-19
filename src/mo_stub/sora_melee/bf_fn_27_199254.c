typedef struct {
    char pad[8];
    int f : 6;
} S;

int fn_27_199254(S* p) {
    return p->f;
}
