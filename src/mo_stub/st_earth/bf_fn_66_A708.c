typedef struct {
    char pad[8];
    unsigned int p0 : 12;
    unsigned int f : 1;
} S;

void fn_66_A708(S* p) {
    p->f = 1;
}
