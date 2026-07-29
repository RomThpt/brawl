typedef struct {
    char pad[356];
    unsigned char p0 : 7;
    unsigned char f : 1;
} S;

void fn_27_1CB00(S* s, unsigned char v) {
    s->f = v;
}
