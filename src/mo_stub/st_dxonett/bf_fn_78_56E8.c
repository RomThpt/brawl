typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 1;
} S;

void fn_78_56E8(S* p) {
    p->f = 0;
}
