typedef struct {
    char pad[309];
    unsigned char p0 : 5;
    unsigned char f : 1;
} S;

void fn_27_9ECC8(S* s, unsigned char v) {
    s->f = v;
}
