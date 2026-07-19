typedef struct {
    char pad[28];
    unsigned int p0 : 30;
    unsigned int f : 1;
} S;

unsigned int fn_90_29C8(S* p) {
    return p->f;
}
