typedef struct {
    char pad[8];
    int f : 2;
} S;

int fn_27_FF084(S* p) {
    return p->f;
}
