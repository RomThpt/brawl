typedef struct {
    char pad[69];
    unsigned char f : 1;
} S;

void fn_41_27740(S* s, unsigned char v) {
    s->f = v;
}
