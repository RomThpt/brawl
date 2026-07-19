typedef struct {
    char pad[8];
    int f : 9;
} S;

int fn_27_CE680(S* p) {
    return p->f;
}
