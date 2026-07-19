typedef struct {
    char pad[8];
    int f : 4;
} S;

int fn_73_A040(S* p) {
    return p->f;
}
