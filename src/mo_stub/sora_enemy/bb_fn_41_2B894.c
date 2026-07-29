typedef struct {
    char pad[80];
    unsigned char p0 : 4;
    unsigned char f : 1;
} S;

void fn_41_2B894(S* s, unsigned char v) {
    s->f = v;
}
