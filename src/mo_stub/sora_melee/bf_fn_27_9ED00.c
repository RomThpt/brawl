typedef struct {
    char pad[12];
    unsigned int f : 1;
} S;

unsigned int fn_27_9ED00(S* p) {
    return p->f;
}
