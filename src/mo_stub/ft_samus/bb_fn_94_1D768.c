typedef struct {
    char pad[164];
    unsigned char p0 : 1;
    unsigned char f : 1;
} S;

void fn_94_1D768(S* s, unsigned char v) {
    s->f = v;
}
