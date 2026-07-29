typedef struct {
    char pad[20];
    unsigned char p0 : 2;
    unsigned char f : 1;
} S;

void fn_27_B4664(S* s, unsigned char v) {
    s->f = v;
}
