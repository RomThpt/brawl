typedef struct {
    char pad[309];
    unsigned char p0 : 4;
    unsigned char f : 1;
} S;

void fn_27_9ECF0(S* s, unsigned char v) {
    s->f = v;
}
