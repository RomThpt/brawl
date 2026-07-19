typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_62_6028(S* p, int v) {
    p->f = v;
}
