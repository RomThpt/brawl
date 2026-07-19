typedef struct {
    char pad[8];
    unsigned int p0 : 3;
    unsigned int f : 3;
} S;

void fn_27_1A5414(S* p, int v) {
    p->f = v;
}
