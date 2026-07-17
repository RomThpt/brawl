int fn_103_133B0(void* p) {
    return *(int*)((char*)p + 8);
}

int fn_103_133B8(void* p) {
    return *(unsigned short*)((char*)p + 22);
}

int fn_103_133C0(void* p) {
    return *(int*)((char*)p + 12);
}

void fn_103_133C8(void* p, int q) {
    *(unsigned short*)((char*)p + 22) = q;
}

void fn_103_133D0(void* p, int q) {
    *(unsigned short*)((char*)p + 20) = q;
}
