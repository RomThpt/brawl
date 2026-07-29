typedef struct {
    char pad[80];
    unsigned char f : 1;
} S;

void fn_27_2E7E8(S* s, unsigned char v) {
    s->f = v;
}
