typedef struct {
    char pad[8];
    unsigned int f : 6;
} S;

void fn_27_1CF83C(S* p, int v) {
    p->f = v;
}
