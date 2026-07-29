typedef struct {
    char pad[68];
    unsigned char p0 : 1;
    unsigned char f : 1;
} S;

void fn_27_132FC(S* s, unsigned char v) {
    s->f = v;
}
