typedef struct {
    char pad[164];
    unsigned char p0 : 1;
    unsigned char f : 1;
} S;

void fn_101_15CAC(S* s, unsigned char v) {
    s->f = v;
}
