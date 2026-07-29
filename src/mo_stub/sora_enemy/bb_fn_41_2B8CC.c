typedef struct {
    char pad[80];
    unsigned char f : 1;
} S;

void fn_41_2B8CC(S* s, unsigned char v) {
    s->f = v;
}
