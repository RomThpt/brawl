typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_71_9E94(S* p, int v) {
    p->f = v;
}
