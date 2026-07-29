typedef struct {
    char pad[84];
    unsigned char f : 1;
} S;

void fn_27_14A38(S* s, unsigned char v) {
    s->f = v;
}
