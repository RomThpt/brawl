typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_54_68DC(S* p) {
    p->f = 1;
}
