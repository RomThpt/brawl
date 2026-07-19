typedef struct {
    char pad[8];
    unsigned int p0 : 18;
    unsigned int f : 1;
} S;

void fn_40_1E44C(S* p) {
    p->f = 1;
}
