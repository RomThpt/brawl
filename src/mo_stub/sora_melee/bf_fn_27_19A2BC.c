typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    int f : 5;
} S;

int fn_27_19A2BC(S* p) {
    return p->f;
}
