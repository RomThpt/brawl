typedef struct {
    char pad[68];
    unsigned char p0 : 3;
    unsigned char f : 1;
} S;

void fn_27_B6D48(S* s, unsigned char v) {
    s->f = v;
}
