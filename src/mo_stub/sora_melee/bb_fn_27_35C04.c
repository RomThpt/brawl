typedef struct {
    char pad[56];
    unsigned char p0 : 1;
    unsigned char f : 1;
} S;

void fn_27_35C04(S* s, unsigned char v) {
    s->f = v;
}
