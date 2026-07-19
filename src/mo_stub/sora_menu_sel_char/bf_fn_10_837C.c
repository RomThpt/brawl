typedef struct {
    char pad[20];
    unsigned int p0 : 23;
    unsigned int f : 1;
} S;

unsigned int fn_10_837C(S* p) {
    return p->f;
}
