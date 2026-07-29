typedef struct {
    char pad[164];
    unsigned char p0 : 1;
    unsigned char f : 1;
} S;

void fn_122_18B9C(S* s, unsigned char v) {
    s->f = v;
}
