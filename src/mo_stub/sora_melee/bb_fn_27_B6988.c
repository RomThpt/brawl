typedef struct {
    char pad[68];
    unsigned char p0 : 4;
    unsigned char f : 2;
} S;

void fn_27_B6988(S* s, unsigned char v) {
    s->f = v;
}
