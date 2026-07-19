typedef struct {
    char pad[8];
    unsigned int p0 : 4;
    int f : 4;
} S;

int fn_76_3FEC(S* p) {
    return p->f;
}
