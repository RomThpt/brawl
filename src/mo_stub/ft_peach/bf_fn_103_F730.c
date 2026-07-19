typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    unsigned int f : 1;
} S;

void fn_103_F730(S* p) {
    p->f = 1;
}
