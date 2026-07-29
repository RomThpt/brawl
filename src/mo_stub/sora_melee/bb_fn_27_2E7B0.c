typedef struct {
    char pad[80];
    unsigned char p0 : 4;
    unsigned char f : 1;
} S;

void fn_27_2E7B0(S* s, unsigned char v) {
    s->f = v;
}
