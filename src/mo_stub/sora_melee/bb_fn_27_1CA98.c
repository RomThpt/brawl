typedef struct {
    char pad[356];
    unsigned char p0 : 1;
    unsigned char f : 1;
} S;

void fn_27_1CA98(S* s, unsigned char v) {
    s->f = v;
}
