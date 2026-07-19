typedef struct {
    char pad[8];
    unsigned int p0 : 15;
    unsigned int f : 1;
} S;

void fn_27_A1C08(S* p) {
    p->f = 1;
}
