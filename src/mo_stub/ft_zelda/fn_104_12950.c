int fn_104_12950(void* p) {
    return *(int*)((char*)p + 8);
}

int fn_104_12958(void* p) {
    return *(unsigned short*)((char*)p + 22);
}

int fn_104_12960(void* p) {
    return *(int*)((char*)p + 12);
}

void fn_104_12968(void* p, int q) {
    *(unsigned short*)((char*)p + 22) = q;
}

void fn_104_12970(void* p, int q) {
    *(unsigned short*)((char*)p + 20) = q;
}
