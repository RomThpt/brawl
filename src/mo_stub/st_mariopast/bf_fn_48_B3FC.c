typedef struct {
    char pad[8];
    int f : 9;
} S;

int fn_48_B3FC(S* p) {
    return p->f;
}
