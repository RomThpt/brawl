void* fn_27_1AF92C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 284) idx -= 284;
    return (char*)p + idx * 4 + 12;
}
