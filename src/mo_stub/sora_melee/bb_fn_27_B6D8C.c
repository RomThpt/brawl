typedef struct {
    char pad[68];
    unsigned char f : 1;
} S;

void fn_27_B6D8C(S* s, unsigned char v) {
    s->f = v;
}
