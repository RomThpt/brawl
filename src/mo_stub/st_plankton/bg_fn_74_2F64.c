typedef struct {
    char pad[108];
    unsigned char p0 : 4;
    unsigned char f : 1;
} S;

unsigned char fn_74_2F64(S* s) {
    return s->f;
}
