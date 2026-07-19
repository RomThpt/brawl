typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 1;
} S;

void fn_71_F6E4(S* p) {
    p->f = 0;
}
