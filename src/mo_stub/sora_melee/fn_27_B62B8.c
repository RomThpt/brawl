extern int fn_27_B5F54();
extern int fn_27_B5F84();

int fn_27_B62B8(void* p) {
    return *(int*)((char*)p + 48);
}

int fn_27_B62C0(void* p) {
    return *(int*)((char*)p + 44);
}

void fn_27_B62C8(void) {
}

int fn_27_B62CC(void* p) {
    return fn_27_B5F54((char*)p + (-8));
}

int fn_27_B62D4(void* p) {
    return fn_27_B5F84((char*)p + (-20));
}
