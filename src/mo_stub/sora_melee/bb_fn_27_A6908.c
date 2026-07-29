typedef struct {
    char pad[69];
    unsigned char f : 1;
} S;

void fn_27_A6908(S* s, unsigned char v) {
    s->f = v;
}
