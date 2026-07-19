typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    int f : 6;
} S;

int fn_27_DB8D4(S* p) {
    return p->f;
}
