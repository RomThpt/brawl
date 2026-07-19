typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_27_2957CC(S* p, int v) {
    p->f = v;
}
