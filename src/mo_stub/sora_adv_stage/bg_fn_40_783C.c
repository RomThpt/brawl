typedef struct {
    char pad[1360];
    unsigned char p0 : 6;
    unsigned char f : 1;
} S;

unsigned char fn_40_783C(S* s) {
    return s->f;
}
