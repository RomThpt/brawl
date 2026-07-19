typedef struct {
    char pad[4];
    unsigned int p0 : 15;
    int f : 5;
} S;

int fn_27_9EE8C(S* p) {
    return p->f;
}
