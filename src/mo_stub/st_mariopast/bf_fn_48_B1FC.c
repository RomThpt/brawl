typedef struct {
    char pad[8];
    int f : 6;
} S;

int fn_48_B1FC(S* p) {
    return p->f;
}
