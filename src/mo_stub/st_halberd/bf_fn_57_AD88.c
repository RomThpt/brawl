typedef struct {
    char pad[8];
    unsigned int f : 3;
} S;

void fn_57_AD88(S* p, int v) {
    p->f = v;
}
