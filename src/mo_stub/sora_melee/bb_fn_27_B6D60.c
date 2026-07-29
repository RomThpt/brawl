typedef struct {
    char pad[68];
    unsigned char p0 : 2;
    unsigned char f : 1;
} S;

void fn_27_B6D60(S* s, unsigned char v) {
    s->f = v;
}
