typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_50_6444(S* p) {
    p->f = 0;
}
