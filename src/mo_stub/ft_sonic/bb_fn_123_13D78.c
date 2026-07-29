typedef struct {
    char pad[164];
    unsigned char p0 : 1;
    unsigned char f : 1;
} S;

void fn_123_13D78(S* s, unsigned char v) {
    s->f = v;
}
