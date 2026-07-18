extern int fn_27_6EAB8();

void fn_27_6F2EC(void* p, int q) {
    *(unsigned short*)((char*)p + 60) = q;
}

int fn_27_6F2F4(void* p) {
    return *(unsigned short*)((char*)p + 60);
}

int fn_27_6F2FC(void* p) {
    return fn_27_6EAB8((char*)p + (-8));
}
