typedef struct {
    char pad[164];
    unsigned char p0 : 1;
    unsigned char f : 1;
} S;

void fn_111_10C04(S* s, unsigned char v) {
    s->f = v;
}
