typedef struct {
    char pad[356];
    unsigned char p0 : 6;
    unsigned char f : 1;
} S;

void fn_27_1CAF0(S* s, unsigned char v) {
    s->f = v;
}
