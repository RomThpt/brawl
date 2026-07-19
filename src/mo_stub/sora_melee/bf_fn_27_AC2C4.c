typedef struct {
    char pad[8];
    int f : 6;
} S;

int fn_27_AC2C4(S* p) {
    return p->f;
}
