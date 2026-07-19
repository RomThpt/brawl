typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 1;
} S;

void fn_51_6444(S* p) {
    p->f = 1;
}
